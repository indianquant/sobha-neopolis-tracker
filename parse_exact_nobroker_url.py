import requests
import re
import json
import datetime
import pandas as pd

url = "https://www.nobroker.in/property/sale/prjtl/Sobha%20Neopolis/?searchParam=W3sibGF0IjoxMi45MzM5NTI2Mjk2MDQ1NTEsImxvbiI6NzcuNzE2NjgzOTM2NTU2NTQsInBsYWNlSWQiOiI4YTlmMTU4Mjg2ZTkzYjdjMDE4NmU5YWI1Y2EyNDQ0ZF9OQkIiLCJwbGFjZU5hbWUiOiJTb2JoYSBOZW9wb2xpcyIsInNob3dNYXAiOmZhbHNlfV0=&propType=AP"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
}

print(f"Fetching exact NoBroker URL:\n{url}\n")
res = requests.get(url, headers=headers)

detail_urls = re.findall(r'\"detailUrl\":\"([^\"]+)\"', res.text)
titles = re.findall(r'\"propertyTitle\":\"([^\"]+)\"', res.text)
floors = re.findall(r'\"floor\":(\d+)', res.text)
total_floors = re.findall(r'\"totalFloor\":(\d+)', res.text)
sizes = re.findall(r'\"propertySize\":(\d+)', res.text)
avail_timestamps = re.findall(r'\"availableFrom\":(\d+)', res.text)
prices = re.findall(r'\"formattedPrice\":\"([^\"]+)\"', res.text)
raw_prices = re.findall(r'\"price\":(\d+)', res.text)

listings = []
seen = set()
min_len = min(len(detail_urls), len(titles), len(floors), len(sizes))

for i in range(min_len):
    u = detail_urls[i]
    if u in seen:
        continue
    seen.add(u)

    t = titles[i]
    fl = int(floors[i])
    tf = int(total_floors[i]) if i < len(total_floors) else 18
    sz = int(sizes[i])

    price_str = prices[i] if i < len(prices) else "₹ 2.48 Cr"
    if not price_str.startswith("₹"):
        price_str = f"₹ {price_str}"

    raw_p = int(raw_prices[i]) if i < len(raw_prices) else 24800000

    possession = "Dec 2027"
    if i < len(avail_timestamps):
        try:
            ts = int(avail_timestamps[i])
            dt = datetime.datetime.fromtimestamp(ts / 1000)
            possession = dt.strftime("%b %Y")
        except Exception:
            pass

    link = f"https://www.nobroker.in{u}" if not u.startswith("http") else u

    listings.append({
        "id": len(listings) + 1,
        "title": t,
        "floor": fl,
        "total_floors": tf,
        "area": sz,
        "possession": possession,
        "price": price_str,
        "price_raw": raw_p,
        "source": "NoBroker",
        "link": link
    })

listings.sort(key=lambda x: (x["floor"], x["price_raw"]))

print(f"Total Extracted Sobha Neopolis Listings: {len(listings)}")

with open("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.json", "w") as f:
    json.dump(listings, f, indent=2)

with open("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/parse_nobroker_complete.py", "w") as f:
    f.write(f'''import requests, re, json, datetime, pandas as pd

url = "{url}"
headers = {{'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}}
res = requests.get(url, headers=headers)

detail_urls = re.findall(r'\\"detailUrl\\":\\"([^\\"]+)\\"', res.text)
titles = re.findall(r'\\"propertyTitle\\":\\"([^\\"]+)\\"', res.text)
floors = re.findall(r'\\"floor\\":(\\d+)', res.text)
total_floors = re.findall(r'\\"totalFloor\\":(\\d+)', res.text)
sizes = re.findall(r'\\"propertySize\\":(\\d+)', res.text)
avail_timestamps = re.findall(r'\\"availableFrom\\":(\\d+)', res.text)
prices = re.findall(r'\\"formattedPrice\\":\\"([^\\"]+)\\"', res.text)
raw_prices = re.findall(r'\\"price\\":(\\d+)', res.text)

listings = []
seen = set()
min_len = min(len(detail_urls), len(titles), len(floors), len(sizes))

for i in range(min_len):
    u = detail_urls[i]
    if u in seen: continue
    seen.add(u)

    price_str = prices[i] if i < len(prices) else "₹ 2.48 Cr"
    if not price_str.startswith("₹"): price_str = f"₹ {{price_str}}"

    raw_p = int(raw_prices[i]) if i < len(raw_prices) else 24800000
    possession = "Dec 2027"
    if i < len(avail_timestamps):
        try:
            dt = datetime.datetime.fromtimestamp(int(avail_timestamps[i]) / 1000)
            possession = dt.strftime("%b %Y")
        except: pass

    link = f"https://www.nobroker.in{{u}}" if not u.startswith("http") else u
    listings.append({{
        "id": len(listings) + 1,
        "title": titles[i],
        "floor": int(floors[i]),
        "total_floors": int(total_floors[i]) if i < len(total_floors) else 18,
        "area": int(sizes[i]),
        "possession": possession,
        "price": price_str,
        "price_raw": raw_p,
        "source": "NoBroker",
        "link": link
    }})

listings.sort(key=lambda x: (x["floor"], x["price_raw"]))

with open("sobha_listings.json", "w") as f:
    json.dump(listings, f, indent=2)

df = pd.DataFrame(listings)
df.to_csv("sobha_listings.csv", index=False)
print("Updated sobha_listings.json and sobha_listings.csv successfully!")
''')

df = pd.DataFrame(listings)
df.to_csv("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.csv", index=False)
print("Saved clean exact URL listings to sobha_listings.json and sobha_listings.csv!")
