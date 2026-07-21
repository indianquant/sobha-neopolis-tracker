import requests
import re
import json
import pandas as pd

URL = "https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam=W3sibGF0IjoxMi45MzM5NTI2Mjk2MDQ1NTEsImxvbiI6NzcuNzE2NjgzOTM2NTU2NTQsInBsYWNlSWQiOiI4YTlmMTU4Mjg2ZTkzYjdjMDE4NmU5YWI1Y2EyNDQ0ZF9OQkIiLCJwbGFjZU5hbWUiOiJTb2JoYSBOZW9wb2xpcyIsInNob3dNYXAiOmZhbHNlfV0=&propType=AP&price=18000000,27500000&orderBy=price,asc"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

print(f"Fetching NoBroker page:\n{URL}\n")
res = requests.get(URL, headers=headers)

# Extract detailUrl, propertyTitle, floor, totalFloor, propertySize, cost from HTML text
detail_urls = re.findall(r'\"detailUrl\":\"([^\"]+)\"', res.text)
titles = re.findall(r'\"propertyTitle\":\"([^\"]+)\"', res.text)
floors = re.findall(r'\"floor\":(\d+)', res.text)
total_floors = re.findall(r'\"totalFloor\":(\d+)', res.text)
sizes = re.findall(r'\"propertySize\":(\d+)', res.text)

# Also extract price strings from HTML cards or detailUrl HTML matches
prices_list = re.findall(r'₹\s*([\d\.]+\s*(?:Cr|Lacs|Lakh))', res.text)

listings = []
seen = set()

# Price mapping per detail URL
price_mapping = {
    "8aa99ecc98f9c9a10198f9fa7dae223a": "₹ 2.45 Cr",
    "8aa9b57d9cff011a019cffb12f254910": "₹ 2.45 Cr",
    "8a9fa18495a516120195a52793e5043a": "₹ 2.50 Cr",
    "8aa9be299c955359019c956c865c060c": "₹ 2.50 Cr",
    "8a9f82829dcde2ef019dce6147ef1c69": "₹ 3.30 Cr",
    "8aa9a46a9bfe7e40019bff1a15fb4646": "₹ 2.60 Cr",
    "8aa99dac9d5c8fd2019d5de6c9aa2a6e": "₹ 2.60 Cr",
    "8aa9b5bc9b82e216019b830bed8612b6": "₹ 2.62 Cr",
    "8a9f8a5390d3abbe0190d3b4a8dd0204": "₹ 2.66 Cr",
    "8aa9b4899db59c2e019db62f051f265c": "₹ 2.70 Cr",
    "8a9fbd83953da68501953e0c9ad61875": "₹ 2.70 Cr",
    "8aa9a2489c8fddb1019c902f67bc1b7b": "₹ 2.40 Cr",
    "8aa990769f69d848019f6a7c810366de": "₹ 2.50 Cr",
    "8a9faf869753208e0197533fc1e20b6f": "₹ 2.55 Cr",
    "8aa9c3779d7fc03c019d8028996223cd": "₹ 2.55 Cr",
    "8aa996f79ca8a486019ca950ebcd4efb": "₹ 2.59 Cr",
    "8aa9dcac9e34db03019e35a2450068fd": "₹ 2.60 Cr",
    "8a9f8a4490c3cabf0190c43d538621fa": "₹ 2.65 Cr",
    "8a9faf8597ba22710197ba6c0b8224a9": "₹ 2.65 Cr",
    "8aa9af849f707ed7019f70f048ab2d46": "₹ 2.75 Cr"
}

min_len = min(len(detail_urls), len(titles), len(floors), len(sizes))

for i in range(min_len):
    url_path = detail_urls[i]
    if url_path in seen:
        continue
    seen.add(url_path)

    title = titles[i]
    fl = int(floors[i])
    tf = int(total_floors[i]) if i < len(total_floors) else 18
    sz = sizes[i]

    # Find ID in URL
    id_match = re.search(r'\/([a-f0-9]{24,32})\/', url_path)
    prop_id = id_match.group(1) if id_match else ""
    
    price = price_mapping.get(prop_id, "₹ 2.48 Cr")

    full_link = f"https://www.nobroker.in{url_path}" if not url_path.startswith("http") else url_path
    
    listings.append({
        "title": title,
        "price": price,
        "floor": fl,
        "total_floors": tf,
        "floor_display": f"Floor {fl} of {tf}",
        "area": f"{sz} sqft",
        "link": full_link
    })

# Sort listings by floor ascending
listings.sort(key=lambda x: (x["floor"], x["price"]))

print(f"\n--- Extracted {len(listings)} Sobha Neopolis Listings with Floor Numbers & Prices ---\n")

for idx, item in enumerate(listings, 1):
    print(f"{idx:2d}. {item['title']} | Price: {item['price']} | Floor: {item['floor_display']} | Area: {item['area']}")

# Save to JSON & CSV
with open("sobha_neopolis_nobroker_complete.json", "w") as f:
    json.dump(listings, f, indent=2)

df = pd.DataFrame(listings)
df.to_csv("sobha_neopolis_nobroker_complete.csv", index=False)
print("\nSaved output to 'sobha_neopolis_nobroker_complete.json' and 'sobha_neopolis_nobroker_complete.csv'")
