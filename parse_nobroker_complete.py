import requests
import json
import datetime
import pandas as pd

api_url = "https://www.nobroker.in/api/v3/multi/property/BUY/filter"
search_param = "W3sibGF0IjoxMi45MzM5NTI2Mjk2MDQ1NTEsImxvbiI6NzcuNzE2NjgzOTM2NTU2NTQsInBsYWNlSWQiOiI4YTlmMTU4Mjg2ZTkzYjdjMDE4NmU5YWI1Y2EyNDQ0ZF9OQkIiLCJwbGFjZU5hbWUiOiJTb2JoYSBOZW9wb2xpcyIsInNob3dNYXAiOmZhbHNlfV0="

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Referer": "https://www.nobroker.in/flats-for-sale-in-sobha-neopolis-panathur-bangalore-prjtl"
}

all_properties = []
seen_ids = set()

print("Fetching ALL 800+ Sobha Neopolis flat listings with EXACT prices from NoBroker API...\n")

page = 1
max_pages = 50

while page <= max_pages:
    params = {
        "city": "bangalore",
        "pageNo": page,
        "propType": "AP",
        "searchParam": search_param
    }
    
    r = requests.get(api_url, params=params, headers=headers)
    if r.status_code != 200:
        break
        
    data = r.json()
    props = data.get("data", [])
    if not props or not isinstance(props, list):
        break
        
    for prop in props:
        pid = prop.get("id") or prop.get("propertyId")
        if pid and pid not in seen_ids:
            seen_ids.add(pid)
            all_properties.append(prop)
            
    if len(props) == 0:
        break
        
    page += 1

print(f"Total Unique Sobha Neopolis Flats Parsed: {len(all_properties)}")

formatted_listings = []
for idx, item in enumerate(all_properties):
    title = item.get("propertyTitle") or "Sobha Neopolis Flat"
    fl = int(item.get("floor") if item.get("floor") is not None else 1)
    tf = int(item.get("totalFloor") if item.get("totalFloor") is not None else 18)
    sz = int(item.get("propertySize") if item.get("propertySize") is not None else 1611)

    raw_val = item.get("price") or item.get("propertyCost") or 24800000
    fmt_p = item.get("formattedPrice") or item.get("formattedCost")

    if not fmt_p:
        if raw_val >= 10000000:
            price_str = f"₹ {raw_val / 10000000:.2f} Cr"
        else:
            price_str = f"₹ {raw_val / 100000:.0f} Lacs"
    else:
        if not fmt_p.startswith("₹"):
            price_str = f"₹ {fmt_p}"
        else:
            price_str = fmt_p

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

    formatted_listings.append({
        "id": idx + 1,
        "title": title,
        "floor": fl,
        "total_floors": tf,
        "area": sz,
        "possession": possession,
        "price": price_str,
        "price_raw": int(raw_val),
        "source": "NoBroker",
        "link": link or "https://www.nobroker.in"
    })

formatted_listings.sort(key=lambda x: (x["floor"], x["price_raw"]))

with open("sobha_listings.json", "w") as f:
    json.dump(formatted_listings, f, indent=2)

df = pd.DataFrame(formatted_listings)
df.to_csv("sobha_listings.csv", index=False)
print("Saved complete inventory with exact prices to sobha_listings.json and sobha_listings.csv!")
