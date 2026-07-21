import json
import pandas as pd

with open('/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.json') as f:
    data = json.load(f)

# Filter for Sobha Neopolis only
clean_listings = []
for item in data:
    title = item.get('title', '')
    if 'sobha neopolis' in title.lower() or 'shobha neopolis' in title.lower():
        clean_listings.append(item)

# Re-index IDs
for idx, item in enumerate(clean_listings):
    item['id'] = idx + 1
    # Standardize price display
    p_str = item.get('price', '')
    if not p_str.startswith('₹'):
        item['price'] = f"₹ {p_str}"

clean_listings.sort(key=lambda x: (x['floor'], x['price_raw']))

print(f"Cleaned Sobha Neopolis Listings Count: {len(clean_listings)}")

with open('/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.json', 'w') as f:
    json.dump(clean_listings, f, indent=2)

df = pd.DataFrame(clean_listings)
df.to_csv('/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.csv', index=False)
print("Updated sobha_listings.json and sobha_listings.csv successfully!")
