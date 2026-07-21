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

print("Fetching ALL 900+ Sobha Neopolis flat listings across all pages from NoBroker API...\n")

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
    print(f"Page {page} Status: {r.status_code}", end=" | ")
    
    if r.status_code != 200:
        print("Stopped (Non-200 status)")
        break
        
    data = r.json()
    props = data.get("data", [])
    if not props or not isinstance(props, list):
        print("No properties returned. Reached end of pagination.")
        break
        
    added = 0
    for prop in props:
        pid = prop.get("id") or prop.get("propertyId")
        if pid and pid not in seen_ids:
            seen_ids.add(pid)
            all_properties.append(prop)
            added += 1
            
    print(f"Batch count: {len(props)}, New unique added: {added}, Total unique so far: {len(all_properties)}")
    
    if len(props) == 0:
        break
        
    page += 1

print(f"\n=======================================================")
print(f"SUCCESS! Total Unique Sobha Neopolis Flats Parsed: {len(all_properties)}")
print(f"=======================================================\n")

# Format into clean json structure
formatted_listings = []
for idx, item in enumerate(all_properties):
    title = item.get("propertyTitle") or "Sobha Neopolis 3 BHK Flat"
    fl = int(item.get("floor") if item.get("floor") is not None else 1)
    tf = int(item.get("totalFloor") if item.get("totalFloor") is not None else 18)
    sz = int(item.get("propertySize") if item.get("propertySize") is not None else 1611)
    price_str = item.get("formattedCost") or "₹ 2.48 Cr"

    # Raw price
    raw_val = 24800000
    p_clean = price_str.replace("₹", "").strip()
    if "Cr" in p_clean:
        try:
            num = float(p_clean.replace("Cr", "").strip())
            raw_val = int(num * 10000000)
        except: pass
    elif "Lacs" in p_clean or "Lakh" in p_clean:
        try:
            num = float(p_clean.replace("Lacs", "").replace("Lakh", "").strip())
            raw_val = int(num * 100000)
        except: pass

    # Possession date
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
        "price_raw": raw_val,
        "source": "NoBroker",
        "link": link or "https://www.nobroker.in"
    })

formatted_listings.sort(key=lambda x: (x["floor"], x["price_raw"]))

with open("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.json", "w") as f:
    json.dump(formatted_listings, f, indent=2)

df = pd.DataFrame(formatted_listings)
df.to_csv("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.csv", index=False)
print("Saved complete inventory to sobha_listings.json and sobha_listings.csv!")
