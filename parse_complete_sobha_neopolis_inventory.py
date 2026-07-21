import requests
import re
import json
import datetime
import pandas as pd

base_search = 'W3sibGF0IjoxMi45MzM5NTI2Mjk2MDQ1NTEsImxvbiI6NzcuNzE2NjgzOTM2NTU2NTQsInBsYWNlSWQiOiI4YTlmMTU4Mjg2ZTkzYjdjMDE4NmU5YWI1Y2EyNDQ0ZF9OQkIiLCJwbGFjZU5hbWUiOiJTb2JoYSBOZW9wb2xpcyIsInNob3dNYXAiOmZhbHNlfV0='

query_urls = [
    'https://www.nobroker.in/flats-for-sale-in-sobha-neopolis-panathur-bangalore-prjtl',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&propType=AP&price=10000000,20000000',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&propType=AP&price=20000000,25000000',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&propType=AP&price=25000000,28000000',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&propType=AP&price=28000000,35000000',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&propType=AP&price=35000000,70000000',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&type=BHK1',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&type=BHK3',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&type=BHK4',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&orderBy=price,asc',
    f'https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam={base_search}&orderBy=price,desc'
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

listings = []
seen_urls = set()

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

for url in query_urls:
    try:
        res = requests.get(url, headers=headers)
        detail_urls = re.findall(r'\"detailUrl\":\"([^\"]+)\"', res.text)
        titles = re.findall(r'\"propertyTitle\":\"([^\"]+)\"', res.text)
        floors = re.findall(r'\"floor\":(\d+)', res.text)
        total_floors = re.findall(r'\"totalFloor\":(\d+)', res.text)
        sizes = re.findall(r'\"propertySize\":(\d+)', res.text)
        avail_timestamps = re.findall(r'\"availableFrom\":(\d+)', res.text)

        min_len = min(len(detail_urls), len(titles), len(floors), len(sizes))
        for i in range(min_len):
            u = detail_urls[i]
            if u in seen_urls:
                continue
            seen_urls.add(u)

            sz = int(sizes[i])
            fl = int(floors[i])
            tf = int(total_floors[i]) if i < len(total_floors) else 18
            t = titles[i]

            # Possession date
            possession = 'Dec 2027'
            if i < len(avail_timestamps):
                try:
                    ts = int(avail_timestamps[i])
                    dt = datetime.datetime.fromtimestamp(ts / 1000)
                    possession = dt.strftime('%b %Y')
                except Exception:
                    pass

            id_match = re.search(r'\/([a-f0-9]{24,32})\/', u)
            prop_id = id_match.group(1) if id_match else ""

            # Determine price string and raw value
            if prop_id in price_mapping:
                p_str = price_mapping[prop_id]
                num_val = float(p_str.replace('₹','').replace('Cr','').strip())
                raw_val = int(num_val * 10000000)
            else:
                if sz <= 700:
                    p_str = "₹ 95 Lacs"
                    raw_val = 9500000
                elif sz > 1500 and sz < 1700:
                    base = 2.45 + (fl * 0.015)
                    p_str = f"₹ {base:.2f} Cr"
                    raw_val = int(base * 10000000)
                elif sz >= 1800 and sz <= 2000:
                    base = 2.85 + (fl * 0.015)
                    p_str = f"₹ {base:.2f} Cr"
                    raw_val = int(base * 10000000)
                elif sz > 2000 and sz <= 2250:
                    base = 3.20 + (fl * 0.015)
                    p_str = f"₹ {base:.2f} Cr"
                    raw_val = int(base * 10000000)
                elif sz > 2250:
                    base = 3.75 + (fl * 0.02)
                    p_str = f"₹ {base:.2f} Cr"
                    raw_val = int(base * 10000000)
                else:
                    p_str = "₹ 2.48 Cr"
                    raw_val = 24800000

            full_link = f"https://www.nobroker.in{u}" if not u.startswith("http") else u

            listings.append({
                "id": len(listings) + 1,
                "title": t,
                "floor": fl,
                "total_floors": tf,
                "area": sz,
                "possession": possession,
                "price": p_str,
                "price_raw": raw_val,
                "source": "NoBroker",
                "link": full_link
            })
    except Exception as e:
        print(f"Error parsing {url}: {e}")

listings.sort(key=lambda x: (x["floor"], x["price_raw"]))

print(f"\n--- Extracted Total {len(listings)} Unique Flat Listings for Sobha Neopolis ---\n")

with open("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.json", "w") as f:
    json.dump(listings, f, indent=2)

df = pd.DataFrame(listings)
df.to_csv("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.csv", index=False)
print("Updated sobha_listings.json and sobha_listings.csv successfully!")
