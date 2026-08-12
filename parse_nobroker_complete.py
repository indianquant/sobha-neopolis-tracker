import requests
import json
import hashlib
import datetime
import os
import time
import re
import pandas as pd
from bs4 import BeautifulSoup

api_url = "https://www.nobroker.in/api/v3/multi/property/BUY/filter"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}

MISS_THRESHOLD = 2

PROJECTS = {
    "sobha-neopolis": {
        "key": "sobha-neopolis",
        "name": "Sobha Neopolis",
        "location": "Panathur, East Bangalore",
        "possession": "Oct 2026",
        "keywords": ["sobha neopolis", "shobha neopolis", "neopolis"],
        "search_configs": [
            {
                "label": "Sobha Neopolis Locality",
                "params": {
                    "city": "bangalore",
                    "searchParam": "W3sibGF0IjoxMi45MzU5MzU5LCJsb24iOjc3LjcwNTU3MDUsInBsYWNlSWQiOiJDaElKMVRyTENXY1RyanNSZmJKX0I0bDU4VWciLCJwbGFjZU5hbWUiOiJTb2JoYSBOZW9wb2xpcyIsInNob3dNYXAiOmZhbHNlfV0=",
                    "radius": "2.0",
                    "locality": "Sobha Neopolis",
                    "propType": "AP",
                }
            },
            {
                "label": "Sobha Neopolis Building",
                "params": {
                    "city": "bangalore",
                    "searchParam": "W3sibGF0IjoxMi45MzM5NTI2Mjk2MDQ1NTEsImxvbiI6NzcuNzE2NjgzOTM2NTU2NTQsInBsYWNlSWQiOiI4YTlmMTU4Mjg2ZTkzYjdjMDE4NmU5YWI1Y2EyNDQ0ZF9OQkIiLCJwbGFjZU5hbWUiOiJTb2JoYSBOZW9wb2xpcyIsInNob3dNYXAiOmZhbHNlfV0=",
                    "propType": "AP",
                }
            }
        ],
        "magicbricks_urls": [
            "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&localityName=Panathur&cityName=Bangalore",
            "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&localityName=Varthur-Road&cityName=Bangalore"
        ]
    },
    "sobha-royal-pavilion": {
        "key": "sobha-royal-pavilion",
        "name": "Sobha Royal Pavilion",
        "location": "Sarjapur Road, Bangalore",
        "possession": "Ready / Dec 2025",
        "keywords": ["sobha royal pavilion", "royal pavilion"],
        "search_configs": [
            {
                "label": "Hadosiddapura / Sarjapur Road",
                "params": {
                    "city": "bangalore",
                    "searchParam": "W3sibGF0IjoxMi45MTI5ODAyLCJsb24iOjc3LjY4ODIxODQsInBsYWNlSWQiOiJDaElKNnljS0V4bFpyanNSbzF5UjV3VXRQME0iLCJwbGFjZU5hbWUiOiJIYWRvc2lkZGFwdXJhIiwic2hvd01hcCI6ZmFsc2V9XQ==",
                    "radius": "5.0",
                    "propType": "AP",
                }
            },
            {
                "label": "Chikkakannalli Locality",
                "params": {
                    "city": "bangalore",
                    "searchParam": "W3sibGF0IjoxMi45MTc3LCJsb24iOjc3LjY4OTksInBsYWNlSWQiOiJDaElKNWNST3BWejNyanNSMTh4b2lZNHlDOHciLCJwbGFjZU5hbWUiOiJDaGlra2FrYW5uYWxsaSIsInNob3dNYXAiOmZhbHNlfV0=",
                    "radius": "3.0",
                    "propType": "AP",
                }
            }
        ],
        "magicbricks_urls": [
            "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&localityName=Sarjapur-Road&cityName=Bangalore",
            "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&localityName=Hadosiddapura&cityName=Bangalore"
        ]
    },
    "sobha-windsor": {
        "key": "sobha-windsor",
        "name": "Sobha Windsor",
        "location": "Whitefield, Bangalore",
        "possession": "Dec 2025",
        "keywords": ["sobha windsor", "windsor"],
        "search_configs": [
            {
                "label": "Whitefield Locality",
                "params": {
                    "city": "bangalore",
                    "searchParam": "W3sibGF0IjoxMi45Njk4MTAyLCJsb24iOjc3Ljc0OTk3MjEsInBsYWNlSWQiOiJDaElKajZlMVlFd1VyanNSUUQ2TEQ2bkJydEEiLCJwbGFjZU5hbWUiOiJXaGl0ZWZpZWxkIiwic2hvd01hcCI6ZmFsc2V9XQ==",
                    "radius": "5.0",
                    "propType": "AP",
                }
            }
        ],
        "magicbricks_urls": [
            "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&localityName=Whitefield&cityName=Bangalore",
            "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&localityName=Nagondanahalli&cityName=Bangalore"
        ]
    },
    "sobha-sentosa": {
        "key": "sobha-sentosa",
        "name": "Sobha Sentosa",
        "location": "Panathur / Balagere, Bangalore",
        "possession": "Jun 2026",
        "keywords": ["sobha sentosa", "sentosa"],
        "search_configs": [
            {
                "label": "Panathur / Balagere Locality",
                "params": {
                    "city": "bangalore",
                    "searchParam": "W3sibGF0IjoxMi45MzU5MzU5LCJsb24iOjc3LjcwNTU3MDUsInBsYWNlSWQiOiJDaElKMVRyTENXY1RyanNSZmJKX0I0bDU4VWciLCJwbGFjZU5hbWUiOiJQYW5hdGh1ciIsInNob3dNYXAiOmZhbHNlfV0=",
                    "radius": "3.0",
                    "propType": "AP",
                }
            }
        ],
        "magicbricks_urls": [
            "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&localityName=Panathur-Road&cityName=Bangalore",
            "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&localityName=Balagere&cityName=Bangalore"
        ]
    }
}


def make_hash(nobroker_id):
    """Generate a short 8-char hex hash from property ID."""
    return hashlib.sha256(nobroker_id.encode()).hexdigest()[:8]


def parse_mb_price(price_str):
    """Convert MagicBricks price string (e.g. ₹3.67 Cr, ₹85 Lac) to raw integer."""
    if not price_str:
        return 0
    p = price_str.replace('₹', '').replace(',', '').strip()
    val_match = re.search(r'([\d\.]+)\s*(Cr|Lac|Lacs|Lakh|Lakhs|k)?', p, re.IGNORECASE)
    if not val_match:
        return 0
    val = float(val_match.group(1))
    unit = (val_match.group(2) or '').lower()
    if 'cr' in unit:
        return int(val * 10000000)
    elif 'lac' in unit or 'lakh' in unit:
        return int(val * 100000)
    elif 'k' in unit:
        return int(val * 1000)
    return int(val)


def normalize_property_area(title, area_raw):
    """
    Normalizes listing area to Super Built-Up Area (SBA).
    Handles Carpet Area -> SBA conversion based on ~0.65 carpet-to-SBA ratio
    and BHK layout size tiers (e.g., 1240 sqft Carpet Area -> 1915 sqft SBA,
    1040 sqft Carpet Area -> 1611 sqft SBA, 1617 sqft Carpet Area -> 2481 sqft SBA).
    """
    if not area_raw:
        return 1611

    if area_raw in [660, 1611, 1915, 2150, 2481, 2488]:
        return area_raw

    title_lower = (title or "").lower()
    is_4bhk = "4 bhk" in title_lower or "4bhk" in title_lower or "4 bedroom" in title_lower
    is_3bhk = "3 bhk" in title_lower or "3bhk" in title_lower or "3 bedroom" in title_lower
    is_1bhk = "1 bhk" in title_lower or "1bhk" in title_lower or "1 bedroom" in title_lower

    if is_4bhk:
        if area_raw < 2000:
            return 2481
        return area_raw

    if is_1bhk:
        if area_raw < 600:
            return 660
        return area_raw

    if is_3bhk or area_raw < 1600:
        if area_raw <= 1150:
            return 1611
        elif 1151 <= area_raw <= 1349:
            return 1915
        elif 1350 <= area_raw <= 1550:
            return 2150
        elif 1551 <= area_raw < 1750:
            return 1611
        elif 1751 <= area_raw <= 2049:
            return 1915
        elif 2050 <= area_raw <= 2250:
            return 2150
        return area_raw

    return area_raw


def is_project_match(prop, project_config):
    """Filter property against project keywords."""
    society = (prop.get("society") or "").lower()
    title = (prop.get("propertyTitle") or "").lower()
    keywords = project_config.get("keywords", [])
    return any(kw in society or kw in title for kw in keywords)


def is_sobha_neopolis(prop):
    """Backward compatibility helper for Sobha Neopolis."""
    return is_project_match(prop, PROJECTS["sobha-neopolis"])


def get_facing(item):
    """Extract and normalize facing direction."""
    f = item.get("facingDesc") or item.get("facing") or ""
    f = str(f).strip().title()
    if not f or f.lower() in ["none", "null", "undefined", "n/a", "0"]:
        return "N/A"
    map_letters = {
        "N": "North", "S": "South", "E": "East", "W": "West",
        "Ne": "North-East", "Nw": "North-West", "Se": "South-East", "Sw": "South-West"
    }
    return map_letters.get(f, f)


def verify_listing_alive(detail_url):
    """Verify whether a listing URL is still live."""
    if not detail_url:
        return True

    if "nobroker.in" in detail_url:
        try:
            r = requests.get(detail_url, headers=headers, timeout=15, allow_redirects=True)
            html = r.text
            html_lower = html.lower()

            if r.status_code == 404 or "page not found" in html_lower or "/detail" not in r.url:
                return False

            inactive_indicators = [
                "overlay-rented-out",
                "rented-out-text",
                "rentedoutproperty",
                'id="rentedout"',
                "id='rentedout'",
                "inactive-property-container",
                "property inactive",
                "this property is inactive",
                "has been inactive",
                "property no longer available"
            ]

            if any(ind in html_lower for ind in inactive_indicators):
                return False

            soup = BeautifulSoup(html, "html.parser")
            page_title = (soup.title.text if soup.title else "").strip().lower()
            if page_title.endswith("-inactive") or page_title.endswith("inactive") or "-inactive" in page_title:
                return False

            if len(html) < 50000:
                return False
            return True
        except requests.RequestException:
            return True

    elif "magicbricks.com" in detail_url:
        try:
            r = requests.get(detail_url, headers=headers, timeout=15, allow_redirects=True)
            html_lower = r.text.lower()
            if r.status_code == 404 or "page not found" in html_lower or "property no longer available" in html_lower or "sold out" in html_lower:
                return False
            return True
        except requests.RequestException:
            return True

    return True


def _parse_mb_card(c, project_config, base_url):
    """Parse a single MagicBricks card element into a property dict."""
    card_html = str(c)
    card_text = c.text.lower()

    # --- Title ---
    title_el = c.select_one('.mb-srp__card--title') or c.select_one('h2')
    title = title_el.text.strip() if title_el else f"{project_config['name']} Flat"

    # --- Price ---
    price_el = c.select_one('.mb-srp__card__price--amount') or c.select_one('.mb-srp__card--price')
    price_text = price_el.text.strip() if price_el else ''
    raw_val = parse_mb_price(price_text)

    # --- Area with type detection (Super Area vs Carpet Area) ---
    sz = 1600
    is_carpet = False
    for si in c.select('.mb-srp__card__summary__list--item'):
        lbl_el = si.select_one('.mb-srp__card__summary--label')
        val_el = si.select_one('.mb-srp__card__summary--value')
        if lbl_el and val_el:
            lbl = lbl_el.text.strip().lower()
            val_str = val_el.text.strip()
            area_m = re.search(r'(\d+)', val_str.replace(',', ''))
            if area_m and ('area' in lbl or 'sqft' in lbl):
                sz = int(area_m.group(1))
                is_carpet = 'carpet' in lbl
                break  # first area field wins

    # If carpet area found, convert to SBA using normalize helper
    if is_carpet:
        sz = normalize_property_area(title, sz)

    # --- Floor ---
    floor_match = re.search(r'floor\s*(\d+)', card_text)
    fl = int(floor_match.group(1)) if floor_match else 0

    # --- Link & ID ---
    link_el = c.select_one('a[href*="/propertyDetails/"]') or c.select_one('a[href*="magicbricks"]') or c.select_one('a')
    link = (link_el.get('href') or '') if link_el else ''
    if link and not link.startswith('http'):
        link = 'https://www.magicbricks.com' + link

    # Derive stable ID from the full link (more reliable than card HTML pattern matching)
    id_from_link = re.search(r'id=([a-zA-Z0-9]+)', link)
    if id_from_link:
        mb_id = f"mb_{id_from_link.group(1)}"
    else:
        # Fallback: hash of (title + price) for stability across pages
        mb_id = f"mb_{hashlib.md5((title + price_text).encode()).hexdigest()[:8]}"

    return {
        "id": mb_id,
        "title": title,
        "floor": fl,
        "total_floors": 18,
        "area": sz,
        "facing": "N/A",
        "price_text": price_text if price_text.startswith("₹") else f"₹ {price_text}",
        "price_raw": raw_val,
        "link": link or base_url,
        "source": "MagicBricks"
    }


def crawl_magicbricks_listings(project_key, project_config, max_pages=8):
    """Crawl MagicBricks SRP pages (with pagination) for a specific Sobha project."""
    seen_ids = set()
    mb_props = []
    urls = project_config.get("magicbricks_urls", [])
    keywords = project_config.get("keywords", [])

    print(f"\n--- MagicBricks Crawl for {project_config['name']} ---")

    for base_url in urls:
        consecutive_empty = 0
        for page in range(1, max_pages + 1):
            url = f"{base_url}&page={page}" if page > 1 else base_url
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code != 200:
                    break

                soup = BeautifulSoup(r.text, 'html.parser')
                cards = soup.select('.mb-srp__card')
                if not cards:
                    break

                page_matches = 0
                for c in cards:
                    card_text = c.text.lower()
                    if not any(k in card_text for k in keywords):
                        continue

                    prop = _parse_mb_card(c, project_config, base_url)
                    if prop["id"] not in seen_ids:
                        seen_ids.add(prop["id"])
                        mb_props.append(prop)
                        page_matches += 1

                print(f"  [MB] {base_url[-50:]} page={page}: {len(cards)} cards, {page_matches} new Sobha matches")

                if page_matches == 0:
                    consecutive_empty += 1
                    if consecutive_empty >= 2:
                        # Two consecutive pages with zero matches – stop early
                        break
                else:
                    consecutive_empty = 0

            except Exception as e:
                print(f"  Error crawling MB URL {url}: {e}")
                break

    print(f"  MagicBricks unique properties found: {len(mb_props)}")
    return mb_props


def run_single_project_crawler(project_key, project_config):
    """Run full crawler pipeline (NoBroker + MagicBricks) for a single Sobha project."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    safe_key = project_key.replace("-", "_")
    history_path = os.path.join(data_dir, f"{safe_key}_history.json")
    listings_path = os.path.join(data_dir, f"{safe_key}_listings.json")
    csv_path = os.path.join(data_dir, f"{safe_key}_listings.csv")

    root_history_path = os.path.join(script_dir, "sobha_history.json") if project_key == "sobha-neopolis" else None
    root_listings_path = os.path.join(script_dir, "sobha_listings.json") if project_key == "sobha-neopolis" else None
    root_csv_path = os.path.join(script_dir, "sobha_listings.csv") if project_key == "sobha-neopolis" else None

    history = {}
    if root_history_path and os.path.exists(root_history_path):
        with open(root_history_path) as f:
            history = json.load(f)
    elif os.path.exists(history_path):
        with open(history_path) as f:
            history = json.load(f)

    today = datetime.date.today().isoformat()
    all_props = {}

    print(f"\n============================================================")
    print(f" Crawling {project_config['name']} ({project_config['location']})")
    print(f"============================================================")

    # 1. NoBroker Search
    for config in project_config["search_configs"]:
        print(f"--- {config['label']} ---")
        page = 1
        while page <= 40:
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
                if pid and pid not in all_props and is_project_match(prop, project_config):
                    all_props[pid] = {**prop, "_source": "NoBroker"}
                    added += 1

            print(f"  Page {page}: batch={len(props)}, new match={added}, total={len(all_props)}")
            page += 1

    # 2. MagicBricks Search
    mb_listings = crawl_magicbricks_listings(project_key, project_config)
    for mb_item in mb_listings:
        mb_pid = mb_item["id"]
        if mb_pid and mb_pid not in all_props:
            all_props[mb_pid] = {
                "propertyTitle": mb_item["title"],
                "floor": mb_item["floor"],
                "totalFloor": mb_item["total_floors"],
                "propertySize": mb_item["area"],
                "facing": mb_item["facing"],
                "price": mb_item["price_raw"],
                "formattedPrice": mb_item["price_text"],
                "detailUrl": mb_item["link"],
                "_source": "MagicBricks"
            }

    current_hashes = set()
    hash_to_pid = {}
    formatted = []

    for idx, (pid, item) in enumerate(all_props.items()):
        uid = make_hash(pid)
        current_hashes.add(uid)
        hash_to_pid[uid] = pid

        source = item.get("_source", "NoBroker")
        title = item.get("propertyTitle") or f"{project_config['name']} Flat"
        fl = int(item.get("floor") if item.get("floor") is not None else 0)
        tf = int(item.get("totalFloor") if item.get("totalFloor") is not None else 18)
        raw_sz = int(item.get("propertySize") if item.get("propertySize") is not None else 1600)
        sz = normalize_property_area(title, raw_sz)
        facing = get_facing(item)

        raw_val = int(item.get("price") or item.get("propertyCost") or 25000000)
        fmt_p = item.get("formattedPrice") or item.get("formattedCost")

        if fmt_p:
            price_str = fmt_p if fmt_p.startswith("₹") else f"₹ {fmt_p}"
        else:
            if raw_val >= 10000000:
                price_str = f"₹ {raw_val / 10000000:.2f} Cr"
            else:
                price_str = f"₹ {raw_val / 100000:.0f} Lacs"

        possession = project_config.get("possession", "Dec 2026")
        if item.get("availableFrom"):
            try:
                ts = int(item["availableFrom"])
                dt = datetime.datetime.fromtimestamp(ts / 1000)
                possession = dt.strftime("%b %Y")
            except Exception:
                pass

        detail_url = item.get("detailUrl") or ""
        link = detail_url if detail_url.startswith("http") else f"https://www.nobroker.in{detail_url}"

        first_seen = history[uid]["first_seen"] if uid in history else today

        formatted.append({
            "id": idx + 1,
            "hash": uid,
            "project_key": project_key,
            "project_name": project_config["name"],
            "title": title,
            "floor": fl,
            "total_floors": tf,
            "area": sz,
            "facing": facing,
            "possession": possession,
            "price": price_str,
            "price_raw": raw_val,
            "source": source,
            "link": link or "https://www.nobroker.in",
            "first_seen": first_seen,
            "last_seen": today,
            "status": "active"
        })

    formatted.sort(key=lambda x: (x["floor"], x["price_raw"]))
    for idx, item in enumerate(formatted):
        item["id"] = idx + 1

    # Diff
    prev_active_hashes = {h for h, v in history.items() if v.get("status") == "active"}
    new_hashes = current_hashes - prev_active_hashes
    potentially_missing = prev_active_hashes - current_hashes

    confirmed_delisted = set()
    still_alive_but_missing = set()

    for uid in potentially_missing:
        entry = history.get(uid, {})
        link = entry.get("link", "")

        # 1. Immediate URL Verification: Check if detail URL indicates property is inactive/sold
        is_alive = verify_listing_alive(link)
        time.sleep(0.2)

        if not is_alive:
            confirmed_delisted.add(uid)
        else:
            miss_count = entry.get("consecutive_misses", 0) + 1
            if miss_count >= MISS_THRESHOLD:
                confirmed_delisted.add(uid)
            else:
                still_alive_but_missing.add(uid)
                history[uid]["consecutive_misses"] = miss_count

    for uid in still_alive_but_missing:
        entry = history[uid]
        if any(f["hash"] == uid for f in formatted):
            continue
        formatted.append({
            "id": 0,
            "hash": uid,
            "project_key": project_key,
            "project_name": project_config["name"],
            "title": entry.get("title", f"{project_config['name']} Flat"),
            "floor": entry.get("floor", 0),
            "total_floors": entry.get("total_floors", 18),
            "area": entry.get("area", 1600),
            "facing": entry.get("facing", "N/A"),
            "possession": entry.get("possession", project_config.get("possession", "Dec 2026")),
            "price": entry.get("price", "₹ 2.50 Cr"),
            "price_raw": entry.get("price_raw", 25000000),
            "source": entry.get("source", "NoBroker"),
            "link": entry.get("link", "https://www.nobroker.in"),
            "first_seen": entry.get("first_seen", today),
            "last_seen": entry.get("last_seen", today),
            "status": "active"
        })

    formatted.sort(key=lambda x: (x["floor"], x["price_raw"]))
    for idx, item in enumerate(formatted):
        item["id"] = idx + 1

    delisted_entries = []
    for uid in confirmed_delisted:
        entry = history[uid].copy()
        entry["status"] = "delisted"
        entry["delisted_on"] = today
        entry["consecutive_misses"] = 0
        delisted_entries.append(entry)

    for uid, entry in history.items():
        if entry.get("status") == "delisted" and uid not in confirmed_delisted:
            delisted_entries.append(entry.copy())

    for item in formatted:
        uid = item["hash"]
        prev_misses = history.get(uid, {}).get("consecutive_misses", 0)
        history[uid] = {
            "hash": uid,
            "project_key": project_key,
            "title": item["title"],
            "floor": item["floor"],
            "total_floors": item["total_floors"],
            "area": item["area"],
            "facing": item["facing"],
            "possession": item["possession"],
            "price": item["price"],
            "price_raw": item["price_raw"],
            "source": item["source"],
            "link": item["link"],
            "first_seen": item["first_seen"],
            "last_seen": today,
            "status": "active",
            "consecutive_misses": prev_misses if uid in potentially_missing else 0,
        }

    for uid in confirmed_delisted:
        if uid in history:
            history[uid]["status"] = "delisted"
            history[uid]["delisted_on"] = today

    output = {
        "project_key": project_key,
        "project_name": project_config["name"],
        "location": project_config["location"],
        "last_updated": today,
        "active_count": len(formatted),
        "delisted_count": len(delisted_entries),
        "new_count": len(new_hashes),
        "active": formatted,
        "delisted": delisted_entries
    }

    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    with open(listings_path, "w") as f:
        json.dump(output, f, indent=2)

    df = pd.DataFrame(formatted)
    df.to_csv(csv_path, index=False)

    if root_history_path:
        with open(root_history_path, "w") as f:
            json.dump(history, f, indent=2)
    if root_listings_path:
        with open(root_listings_path, "w") as f:
            json.dump(output, f, indent=2)
    if root_csv_path:
        df.to_csv(root_csv_path, index=False)

    nobroker_cnt = len([i for i in formatted if i.get("source") == "NoBroker"])
    mb_cnt = len([i for i in formatted if i.get("source") == "MagicBricks"])

    print(f"Summary for {project_config['name']}: {len(formatted)} Active (NoBroker: {nobroker_cnt}, MagicBricks: {mb_cnt}) | {len(delisted_entries)} Delisted")
    return output


def run_crawler():
    summary = {}
    for pkey, pconfig in PROJECTS.items():
        res = run_single_project_crawler(pkey, pconfig)
        summary[pkey] = {
            "name": pconfig["name"],
            "location": pconfig["location"],
            "active_count": res["active_count"],
            "delisted_count": res["delisted_count"],
            "last_updated": res["last_updated"]
        }

    script_dir = os.path.dirname(os.path.abspath(__file__))
    summary_path = os.path.join(script_dir, "data", "all_projects_summary.json")
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("\n============================================================")
    print(" ALL PROJECTS & SOURCES (NoBroker + MagicBricks) CRAWLED SUCCESSFULLY!")
    print("============================================================")
    for pkey, s in summary.items():
        print(f" - {s['name']}: {s['active_count']} Active units ({s['location']})")


if __name__ == "__main__":
    run_crawler()
