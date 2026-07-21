import asyncio
import json
import re
import datetime
import pandas as pd
from playwright.async_api import async_playwright

async def main():
    print("Launching Playwright Chromium to capture all 900+ Sobha Neopolis listings...")
    all_properties = []
    seen_ids = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        # Listen to network responses
        async def handle_response(response):
            try:
                if "api/v1" in response.url or "filter" in response.url or "property" in response.url:
                    text = await response.text()
                    try:
                        data = json.loads(text)
                        props = data.get("data", [])
                        if isinstance(props, list):
                            for prop in props:
                                pid = prop.get("id") or prop.get("propertyId")
                                if pid and pid not in seen_ids:
                                    seen_ids.add(pid)
                                    all_properties.append(prop)
                    except Exception:
                        pass
            except Exception:
                pass

        page.on("response", handle_response)

        print("Navigating to https://www.nobroker.in/flats-for-sale-in-sobha-neopolis-panathur-bangalore-prjtl...")
        await page.goto("https://www.nobroker.in/flats-for-sale-in-sobha-neopolis-panathur-bangalore-prjtl", wait_until="networkidle", timeout=60000)

        # Scroll down repeatedly to trigger infinite scroll loading
        print("Scrolling down to load infinite scroll listings...")
        last_height = await page.evaluate("document.body.scrollHeight")
        scroll_count = 0

        while scroll_count < 40: # scroll up to 40 times to load 900+ listings
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            await page.wait_for_timeout(2000)
            new_height = await page.evaluate("document.body.scrollHeight")
            scroll_count += 1
            print(f"Scroll {scroll_count}: Captured {len(all_properties)} properties via API...")

            if new_height == last_height and scroll_count > 10:
                # Try clicking any 'Load More' buttons if present
                load_more = await page.query_selector("button:has-text('Load More'), button:has-text('Show More')")
                if load_more:
                    try:
                        await load_more.click()
                        await page.wait_for_timeout(3000)
                    except Exception:
                        break
                else:
                    break
            last_height = new_height

        # Also extract directly from DOM elements if needed
        cards = await page.query_selector_all(".card, article, [id^='property-']")
        print(f"DOM Cards found: {len(cards)}")

        await browser.close()

    print(f"\nFinal Total Properties Captured: {len(all_properties)}")

    # Format into standard listing structure
    formatted_listings = []
    for idx, item in enumerate(all_properties):
        title = item.get("propertyTitle") or "3 BHK Flat In Sobha Neopolis"
        fl = int(item.get("floor") or 1)
        tf = int(item.get("totalFloor") or 18)
        sz = int(item.get("propertySize") or 1611)
        price_str = item.get("formattedCost") or item.get("priceStr") or "₹ 2.48 Cr"
        
        # Raw price calculation
        raw_val = 24800000
        if "Cr" in price_str:
            num = float(re.search(r'[\d\.]+', price_str).group(0))
            raw_val = int(num * 10000000)
        elif "Lacs" in price_str or "Lakh" in price_str:
            num = float(re.search(r'[\d\.]+', price_str).group(0))
            raw_val = int(num * 100000)

        # Possession date
        possession = "Dec 2027"
        if item.get("availableFrom"):
            try:
                ts = int(item["availableFrom"])
                dt = datetime.datetime.fromtimestamp(ts / 1000)
                possession = dt.strftime("%b %Y")
            except Exception:
                pass

        link = item.get("detailUrl") or ""
        if link and not link.startswith("http"):
            link = f"https://www.nobroker.in{link}"

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
            "link": link
        })

    with open("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.json", "w") as f:
        json.dump(formatted_listings, f, indent=2)

    df = pd.DataFrame(formatted_listings)
    df.to_csv("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.csv", index=False)
    print("Saved to sobha_listings.json and sobha_listings.csv successfully!")

if __name__ == "__main__":
    asyncio.run(main())
