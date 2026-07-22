import requests
import json
import hashlib
import datetime
import os
import time
import pandas as pd

api_url = "https://www.nobroker.in/api/v3/multi/property/BUY/filter"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}

SEARCH_CONFIGS = [
    {
        "label": "User URL (locality search)",
        "params": {
            "city": "bangalore",
            "searchParam": "W3sibGF0IjoxMi45MzU5MzU5LCJsb24iOjc3LjcwNTU3MDUsInBsYWNlSWQiOiJDaElKMVRyTENXY1RyanNSZmJKX0I0bDU4VWciLCJwbGFjZU5hbWUiOiJTb2JoYSBOZW9wb2xpcyIsInNob3dNYXAiOmZhbHNlfV0=",
            "radius": "2.0",
            "locality": "Sobha Neopolis",
            "propType": "AP",
        }
    },
    {
        "label": "Project page (prjtl search)",
        "params": {
            "city": "bangalore",
            "searchParam": "W3sibGF0IjoxMi45MzM5NTI2Mjk2MDQ1NTEsImxvbiI6NzcuNzE2NjgzOTM2NTU2NTQsInBsYWNlSWQiOiI4YTlmMTU4Mjg2ZTkzYjdjMDE4NmU5YWI1Y2EyNDQ0ZF9OQkIiLCJwbGFjZU5hbWUiOiJTb2JoYSBOZW9wb2xpcyIsInNob3dNYXAiOmZhbHNlfV0=",
            "propType": "AP",
        }
    },
]

# ── How many consecutive API misses before we verify via URL ──
# A listing must be missing from API results for MISS_THRESHOLD consecutive
# runs before we even bother checking the detail URL.  This prevents
# premature verification calls caused by NoBroker pagination jitter.
MISS_THRESHOLD = 2


def make_hash(nobroker_id):
    """Generate a short 8-char hex hash from the NoBroker property ID."""
    return hashlib.sha256(nobroker_id.encode()).hexdigest()[:8]


def is_sobha_neopolis(prop):
    """Filter: only keep Sobha Neopolis properties."""
    society = (prop.get("society") or "").lower()
    title = (prop.get("propertyTitle") or "").lower()
    return ("sobha neopolis" in society or "shobha neopolis" in society or
            "sobha neopolis" in title or "shobha neopolis" in title)


def verify_listing_alive(detail_url):
    """
    Verify whether a NoBroker listing is still live by fetching
    its detail page HTML.

    Returns True if still alive, False if confirmed dead/expired.

    Verification signals:
      - Live listing HTML is typically >100KB and contains project name
      - Dead/expired listing HTML is typically <50KB, may contain '404',
        or redirects to a different page
    """
    if not detail_url or "nobroker.in" not in detail_url:
        return True  # Can't verify → assume alive (safe default)

    try:
        r = requests.get(
            detail_url,
            headers=headers,
            timeout=15,
            allow_redirects=True,
        )

        html = r.text
        html_len = len(html)
        html_lower = html.lower()

        # Signal 1: Tiny page = error / 404 page
        if html_len < 50000:
            # Check for explicit 404/error signals in the small page
            dead_signals = [
                "page not found",
                "404",
                "this property is currently unavailable",
                "listing has expired",
                "no longer available",
                "property has been removed",
                "deactivated",
            ]
            for signal in dead_signals:
                if signal in html_lower:
                    return False  # Confirmed dead
            # Small page without clear signals — still suspicious
            # but we'll assume alive as a safe default
            return True

        # Signal 2: Large page but redirected away from the detail URL
        if "/detail" not in r.url:
            return False  # Redirected away from detail page

        # Signal 3: Large page with the project name = definitely alive
        if "sobha neopolis" in html_lower or "shobha neopolis" in html_lower:
            return True

        # Signal 4: Large page with property detail markers
        if "propertytitle" in html_lower or "property-detail" in html_lower:
            return True

        # Default: large page, no clear dead signals → assume alive
        return True

    except requests.RequestException:
        return True  # Network error → assume alive (don't wrongly delist)


# ── Load previous history ────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
history_path = os.path.join(script_dir, "sobha_history.json")
listings_path = os.path.join(script_dir, "sobha_listings.json")
csv_path = os.path.join(script_dir, "sobha_listings.csv")

history = {}
if os.path.exists(history_path):
    with open(history_path) as f:
        history = json.load(f)

today = datetime.date.today().isoformat()  # e.g. "2026-07-21"

# ── Fetch all listings from API ──────────────────────────────────
all_props = {}  # keyed by NoBroker property ID

print("Fetching ALL Sobha Neopolis listings from NoBroker...\n")

for config in SEARCH_CONFIGS:
    print(f"--- {config['label']} ---")
    page = 1
    while page <= 50:
        params = {**config["params"], "pageNo": page}
        try:
            r = requests.get(api_url, params=params, headers=headers, timeout=15)
        except requests.RequestException as e:
            print(f"  Page {page}: Network error ({e}), stopping this config.")
            break
        if r.status_code != 200:
            break
        data = r.json()
        props = data.get("data", [])
        if not props:
            break

        added = 0
        for prop in props:
            pid = prop.get("id") or prop.get("propertyId")
            if pid and pid not in all_props and is_sobha_neopolis(prop):
                all_props[pid] = prop
                added += 1

        print(f"  Page {page}: batch={len(props)}, new Neopolis={added}, total={len(all_props)}")
        page += 1
    print()

print(f"{'='*60}")
print(f"TOTAL UNIQUE Sobha Neopolis Flats from API: {len(all_props)}")
print(f"{'='*60}\n")

# ── Build formatted listings with hashes ─────────────────────────
current_hashes = set()
# Map hash → NoBroker property ID (needed for URL building)
hash_to_pid = {}
formatted = []

for idx, (pid, item) in enumerate(all_props.items()):
    uid = make_hash(pid)
    current_hashes.add(uid)
    hash_to_pid[uid] = pid

    title = item.get("propertyTitle") or "Sobha Neopolis Flat"
    fl = int(item.get("floor") if item.get("floor") is not None else 0)
    tf = int(item.get("totalFloor") if item.get("totalFloor") is not None else 18)
    sz = int(item.get("propertySize") if item.get("propertySize") is not None else 1611)

    raw_val = int(item.get("price") or item.get("propertyCost") or 24800000)
    fmt_p = item.get("formattedPrice") or item.get("formattedCost")

    if fmt_p:
        price_str = fmt_p if fmt_p.startswith("₹") else f"₹ {fmt_p}"
    else:
        if raw_val >= 10000000:
            price_str = f"₹ {raw_val / 10000000:.2f} Cr"
        else:
            price_str = f"₹ {raw_val / 100000:.0f} Lacs"

    possession = "Dec 2027"
    if item.get("availableFrom"):
        try:
            ts = int(item["availableFrom"])
            dt = datetime.datetime.fromtimestamp(ts / 1000)
            possession = dt.strftime("%b %Y")
        except Exception:
            pass

    detail_url = item.get("detailUrl") or ""
    link = f"https://www.nobroker.in{detail_url}" if detail_url and not detail_url.startswith("http") else detail_url

    # ── History tracking ──
    if uid in history:
        first_seen = history[uid]["first_seen"]
    else:
        first_seen = today

    formatted.append({
        "id": idx + 1,
        "hash": uid,
        "title": title,
        "floor": fl,
        "total_floors": tf,
        "area": sz,
        "possession": possession,
        "price": price_str,
        "price_raw": raw_val,
        "source": "NoBroker",
        "link": link or "https://www.nobroker.in",
        "first_seen": first_seen,
        "last_seen": today,
        "status": "active"
    })

formatted.sort(key=lambda x: (x["floor"], x["price_raw"]))
for idx, item in enumerate(formatted):
    item["id"] = idx + 1

# ── Diff: identify potentially missing listings ─────────────────
prev_active_hashes = {h for h, v in history.items() if v.get("status") == "active"}
new_hashes = current_hashes - prev_active_hashes
potentially_missing = prev_active_hashes - current_hashes

print(f"Listings diff vs previous run:")
print(f"  ✅ Still in API:       {len(current_hashes & prev_active_hashes)}")
print(f"  🆕 Newly added:        {len(new_hashes)}")
print(f"  ❓ Missing from API:   {len(potentially_missing)}")

# ── ROBUST VERIFICATION: Don't blindly delist! ──────────────────
# For each "missing" listing, increment a miss counter.
# Only attempt URL verification after MISS_THRESHOLD consecutive misses.
# Only mark as delisted if the URL verification CONFIRMS it's dead.

confirmed_delisted = set()
still_alive_but_missing = set()

if potentially_missing:
    print(f"\n--- Verifying {len(potentially_missing)} missing listings ---")

for uid in potentially_missing:
    entry = history.get(uid, {})
    miss_count = entry.get("consecutive_misses", 0) + 1

    if miss_count < MISS_THRESHOLD:
        # Not enough consecutive misses — keep as active, just bump counter
        still_alive_but_missing.add(uid)
        history[uid]["consecutive_misses"] = miss_count
        history[uid]["last_seen"] = entry.get("last_seen", today)
        print(f"  {uid}: Miss #{miss_count} (threshold={MISS_THRESHOLD}) — keeping active, skipping URL check")
        continue

    # Enough misses — now verify via the actual listing URL
    link = entry.get("link", "")
    print(f"  {uid}: Miss #{miss_count} ≥ threshold — verifying URL: {link[:80]}...", end=" ")

    is_alive = verify_listing_alive(link)
    time.sleep(0.5)  # Be polite to NoBroker servers

    if is_alive:
        still_alive_but_missing.add(uid)
        # Reset miss counter since URL confirms it's alive
        history[uid]["consecutive_misses"] = 0
        history[uid]["last_seen"] = today
        print("✅ STILL ALIVE (URL confirmed) — keeping active")
    else:
        confirmed_delisted.add(uid)
        print("❌ CONFIRMED DEAD (URL verified) — marking delisted")

print(f"\n  📊 Verification results:")
print(f"     Still alive (URL-confirmed or under threshold): {len(still_alive_but_missing)}")
print(f"     Confirmed delisted (URL-verified dead):         {len(confirmed_delisted)}")

# ── Add still-alive-but-missing listings back to formatted ──────
# These are listings the API didn't return but URL confirms are still live.
# We keep them in the active list using their historical data.
for uid in still_alive_but_missing:
    entry = history[uid]
    # Check if already in formatted (shouldn't be, but safety check)
    if any(f["hash"] == uid for f in formatted):
        continue
    formatted.append({
        "id": 0,  # Will be re-indexed
        "hash": uid,
        "title": entry.get("title", "Sobha Neopolis Flat"),
        "floor": entry.get("floor", 0),
        "total_floors": entry.get("total_floors", 18),
        "area": entry.get("area", 1611),
        "possession": entry.get("possession", "Dec 2027"),
        "price": entry.get("price", "₹ 2.50 Cr"),
        "price_raw": entry.get("price_raw", 25000000),
        "source": "NoBroker",
        "link": entry.get("link", "https://www.nobroker.in"),
        "first_seen": entry.get("first_seen", today),
        "last_seen": entry.get("last_seen", today),
        "status": "active"
    })

# Re-sort and re-index
formatted.sort(key=lambda x: (x["floor"], x["price_raw"]))
for idx, item in enumerate(formatted):
    item["id"] = idx + 1

# ── Build delisted entries from CONFIRMED delisted only ─────────
delisted_entries = []
for uid in confirmed_delisted:
    entry = history[uid].copy()
    entry["status"] = "delisted"
    entry["delisted_on"] = today
    delisted_entries.append(entry)

# Also include previously-confirmed delisted entries from history
for uid, entry in history.items():
    if entry.get("status") == "delisted" and uid not in confirmed_delisted:
        delisted_entries.append(entry.copy())

# ── Update history ──────────────────────────────────────────────
# Update active listings in history
for item in formatted:
    uid = item["hash"]
    prev = history.get(uid, {})
    history[uid] = {
        "hash": uid,
        "title": item["title"],
        "floor": item["floor"],
        "total_floors": item["total_floors"],
        "area": item["area"],
        "possession": item["possession"],
        "price": item["price"],
        "price_raw": item["price_raw"],
        "link": item["link"],
        "first_seen": item["first_seen"],
        "last_seen": today,
        "status": "active",
        "consecutive_misses": 0,  # Reset — we saw it this run (or URL-confirmed)
    }

# Mark confirmed-delisted in history
for uid in confirmed_delisted:
    if uid in history:
        history[uid]["status"] = "delisted"
        history[uid]["delisted_on"] = today

with open(history_path, "w") as f:
    json.dump(history, f, indent=2)

# ── Save listings JSON (active + delisted section) ──────────────
output = {
    "last_updated": today,
    "active_count": len(formatted),
    "delisted_count": len(delisted_entries),
    "new_count": len(new_hashes),
    "active": formatted,
    "delisted": delisted_entries
}

with open(listings_path, "w") as f:
    json.dump(output, f, indent=2)

df = pd.DataFrame(formatted)
df.to_csv(csv_path, index=False)

# Category breakdown
bhk1 = [i for i in formatted if i["area"] < 1000]
c1611 = [i for i in formatted if 1000 <= i["area"] <= 1750]
c1915 = [i for i in formatted if 1750 < i["area"] <= 2049]
c2150 = [i for i in formatted if 2050 <= i["area"] <= 2250]
c4bhk = [i for i in formatted if i["area"] > 2250]

print(f"\n{'='*60}")
print(f"FINAL INVENTORY")
print(f"{'='*60}")
print(f"1 BHK (<1000 sqft):     {len(bhk1)} units")
print(f"1611 sqft (1000-1750):  {len(c1611)} units")
print(f"1915 sqft (1751-2049):  {len(c1915)} units")
print(f"2150 sqft (2050-2250):  {len(c2150)} units")
print(f"4 BHK (>2250 sqft):    {len(c4bhk)} units")
print(f"TOTAL ACTIVE:           {len(formatted)} units")
print(f"TOTAL DELISTED:         {len(delisted_entries)} units")
print(f"\nSaved sobha_listings.json, sobha_history.json, and sobha_listings.csv!")
