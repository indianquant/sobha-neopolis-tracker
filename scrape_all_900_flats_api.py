import requests
import json
import hashlib
import datetime
import os
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


def make_hash(nobroker_id):
    """Generate a short 8-char hex hash from the NoBroker property ID."""
    return hashlib.sha256(nobroker_id.encode()).hexdigest()[:8]


def is_sobha_neopolis(prop):
    """Filter: only keep Sobha Neopolis properties."""
    society = (prop.get("society") or "").lower()
    title = (prop.get("propertyTitle") or "").lower()
    return ("sobha neopolis" in society or "shobha neopolis" in society or
            "sobha neopolis" in title or "shobha neopolis" in title)


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

# ── Fetch all listings ───────────────────────────────────────────
all_props = {}  # keyed by NoBroker property ID

print("Fetching ALL Sobha Neopolis listings from NoBroker...\n")

for config in SEARCH_CONFIGS:
    print(f"--- {config['label']} ---")
    page = 1
    while page <= 50:
        params = {**config["params"], "pageNo": page}
        r = requests.get(api_url, params=params, headers=headers)
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
print(f"TOTAL UNIQUE Sobha Neopolis Flats: {len(all_props)}")
print(f"{'='*60}\n")

# ── Build formatted listings with hashes ─────────────────────────
current_hashes = set()
formatted = []

for idx, (pid, item) in enumerate(all_props.items()):
    uid = make_hash(pid)
    current_hashes.add(uid)

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

# ── Diff against previous run ───────────────────────────────────
prev_hashes = {h for h, v in history.items() if v.get("status") == "active"}
new_hashes = current_hashes - prev_hashes
delisted_hashes = prev_hashes - current_hashes

print(f"Listings diff vs previous run:")
print(f"  ✅ Still active:  {len(current_hashes & prev_hashes)}")
print(f"  🆕 Newly added:   {len(new_hashes)}")
print(f"  ❌ Delisted/Sold: {len(delisted_hashes)}")

# ── Build delisted entries from history ──────────────────────────
delisted_entries = []
for uid in delisted_hashes:
    entry = history[uid].copy()
    entry["status"] = "delisted"
    entry["last_seen"] = history[uid].get("last_seen", today)
    delisted_entries.append(entry)

# ── Update history ──────────────────────────────────────────────
# Update active listings in history
for item in formatted:
    uid = item["hash"]
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
        "status": "active"
    }

# Mark delisted ones
for uid in delisted_hashes:
    if uid in history:
        history[uid]["status"] = "delisted"

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

print(f"\n1 BHK (<1000 sqft):     {len(bhk1)} units")
print(f"1611 sqft (1000-1750):  {len(c1611)} units")
print(f"1915 sqft (1751-2049):  {len(c1915)} units")
print(f"2150 sqft (2050-2250):  {len(c2150)} units")
print(f"4 BHK (>2250 sqft):    {len(c4bhk)} units")
print(f"TOTAL:                  {len(formatted)} units")
print(f"\nSaved sobha_listings.json, sobha_history.json, and sobha_listings.csv!")
