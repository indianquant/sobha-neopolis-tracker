import requests
import json
import datetime
import pandas as pd

api_url = "https://www.nobroker.in/api/v3/multi/property/BUY/filter"
headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}

# Two searchParams that together cover all Sobha Neopolis listings
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

def is_sobha_neopolis(prop):
    """Filter: only keep Sobha Neopolis properties."""
    society = (prop.get("society") or "").lower()
    title = (prop.get("propertyTitle") or "").lower()
    return ("sobha neopolis" in society or "shobha neopolis" in society or
            "sobha neopolis" in title or "shobha neopolis" in title)

all_props = {}  # keyed by property ID

print("Fetching ALL Sobha Neopolis listings from NoBroker (combined two search endpoints)...\n")

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

# Format into clean JSON
formatted = []
for idx, (pid, item) in enumerate(all_props.items()):
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

    formatted.append({
        "id": idx + 1,
        "title": title,
        "floor": fl,
        "total_floors": tf,
        "area": sz,
        "possession": possession,
        "price": price_str,
        "price_raw": raw_val,
        "source": "NoBroker",
        "link": link or "https://www.nobroker.in"
    })

formatted.sort(key=lambda x: (x["floor"], x["price_raw"]))
for idx, item in enumerate(formatted):
    item["id"] = idx + 1

with open("sobha_listings.json", "w") as f:
    json.dump(formatted, f, indent=2)

df = pd.DataFrame(formatted)
df.to_csv("sobha_listings.csv", index=False)

# Category breakdown
bhk1 = [i for i in formatted if i["area"] < 1000]
c1611 = [i for i in formatted if 1000 <= i["area"] <= 1750]
c1915 = [i for i in formatted if 1750 < i["area"] <= 2049]
c2150 = [i for i in formatted if 2050 <= i["area"] <= 2250]
c4bhk = [i for i in formatted if i["area"] > 2250]

print(f"1 BHK (<1000 sqft):     {len(bhk1)} units")
print(f"1611 sqft (1000-1750):  {len(c1611)} units")
print(f"1915 sqft (1751-2049):  {len(c1915)} units")
print(f"2150 sqft (2050-2250):  {len(c2150)} units")
print(f"4 BHK (>2250 sqft):    {len(c4bhk)} units")
print(f"TOTAL:                  {len(formatted)} units")
print("\nSaved to sobha_listings.json and sobha_listings.csv!")
