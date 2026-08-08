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

MISS_THRESHOLD = 2

PROJECTS = {
    "sobha-neopolis": {
        "key": "sobha-neopolis",
        "name": "Sobha Neopolis",
        "location": "Panathur, East Bangalore",
        "possession": "Oct 2026",
        "keywords": ["sobha neopolis", "shobha neopolis"],
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
        ]
    },
    "sobha-windsor": {
        "key": "sobha-windsor",
        "name": "Sobha Windsor",
        "location": "Whitefield, Bangalore",
        "possession": "Dec 2025",
        "keywords": ["sobha windsor"],
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
        ]
    }
}


def make_hash(nobroker_id):
    """Generate a short 8-char hex hash from the NoBroker property ID."""
    return hashlib.sha256(nobroker_id.encode()).hexdigest()[:8]


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
    """Extract and normalize facing direction (e.g., East, West, North, South, North-East)."""
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
    """
    Verify whether a NoBroker listing is still live by fetching its detail page HTML.
    Returns True if still alive, False if confirmed dead/expired/inactive.
    """
    if not detail_url or "nobroker.in" not in detail_url:
        return True

    try:
        r = requests.get(
            detail_url,
            headers=headers,
            timeout=15,
            allow_redirects=True,
        )
        html = r.text
        html_lower = html.lower()

        # Signal 1: NoBroker exact DOM overlay / banner for inactive flats
        if "rented-out-text" in html or "rentedoutproperty" in html or 'id="rentedout"' in html or "id='rentedout'" in html:
            return False

        # Signal 2: Check for explicit "has been inactive" text banner
        if "has been inactive" in html_lower or "this property is inactive" in html_lower:
            return False

        # Signal 3: Redirected away from the property detail page
        if "/detail" not in r.url:
            return False

        # Signal 4: HTTP 404 or explicit page not found
        if r.status_code == 404 or "page not found" in html_lower:
            return False

        # Signal 5: Tiny page (<50KB) without property title
        if len(html) < 50000:
            return False

        return True

    except requests.RequestException:
        return True


def run_single_project_crawler(project_key, project_config):
    """Run full crawler pipeline for a single Sobha project."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # File paths
    safe_key = project_key.replace("-", "_")
    history_path = os.path.join(data_dir, f"{safe_key}_history.json")
    listings_path = os.path.join(data_dir, f"{safe_key}_listings.json")
    csv_path = os.path.join(data_dir, f"{safe_key}_listings.csv")

    # Maintain root paths for sobha-neopolis backward compatibility
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
                    all_props[pid] = prop
                    added += 1

            print(f"  Page {page}: batch={len(props)}, new match={added}, total={len(all_props)}")
            page += 1

    current_hashes = set()
    hash_to_pid = {}
    formatted = []

    for idx, (pid, item) in enumerate(all_props.items()):
        uid = make_hash(pid)
        current_hashes.add(uid)
        hash_to_pid[uid] = pid

        title = item.get("propertyTitle") or f"{project_config['name']} Flat"
        fl = int(item.get("floor") if item.get("floor") is not None else 0)
        tf = int(item.get("totalFloor") if item.get("totalFloor") is not None else 18)
        sz = int(item.get("propertySize") if item.get("propertySize") is not None else 1600)
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
        link = f"https://www.nobroker.in{detail_url}" if detail_url and not detail_url.startswith("http") else detail_url

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
            "source": "NoBroker",
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
        miss_count = entry.get("consecutive_misses", 0) + 1

        if miss_count < MISS_THRESHOLD:
            still_alive_but_missing.add(uid)
            history[uid]["consecutive_misses"] = miss_count
            history[uid]["last_seen"] = entry.get("last_seen", today)
            continue

        link = entry.get("link", "")
        is_alive = verify_listing_alive(link)
        time.sleep(0.3)

        if is_alive:
            still_alive_but_missing.add(uid)
            history[uid]["consecutive_misses"] = 0
            history[uid]["last_seen"] = today
        else:
            confirmed_delisted.add(uid)

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
            "source": "NoBroker",
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
        delisted_entries.append(entry)

    for uid, entry in history.items():
        if entry.get("status") == "delisted" and uid not in confirmed_delisted:
            delisted_entries.append(entry.copy())

    for item in formatted:
        uid = item["hash"]
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
            "link": item["link"],
            "first_seen": item["first_seen"],
            "last_seen": today,
            "status": "active",
            "consecutive_misses": 0,
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

    # Save to data directory
    with open(history_path, "w") as f:
        json.dump(history, f, indent=2)

    with open(listings_path, "w") as f:
        json.dump(output, f, indent=2)

    df = pd.DataFrame(formatted)
    df.to_csv(csv_path, index=False)

    # If sobha-neopolis, also save to root files for backward compatibility
    if root_history_path:
        with open(root_history_path, "w") as f:
            json.dump(history, f, indent=2)
    if root_listings_path:
        with open(root_listings_path, "w") as f:
            json.dump(output, f, indent=2)
    if root_csv_path:
        df.to_csv(root_csv_path, index=False)

    print(f"Summary for {project_config['name']}: {len(formatted)} Active | {len(delisted_entries)} Delisted")
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
    print(" ALL PROJECTS CRAWLED SUCCESSFULLY!")
    print("============================================================")
    for pkey, s in summary.items():
        print(f" - {s['name']}: {s['active_count']} Active units ({s['location']})")


if __name__ == "__main__":
    run_crawler()
