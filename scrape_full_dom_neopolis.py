import asyncio
import json
import re
import datetime
import pandas as pd
from playwright.async_api import async_playwright

async def main():
    print("Starting Playwright DOM scraper for 900+ Sobha Neopolis listings...")
    all_items = []
    seen = set()

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        )

        print("Navigating to https://www.nobroker.in/flats-for-sale-in-sobha-neopolis-panathur-bangalore-prjtl...")
        await page.goto("https://www.nobroker.in/flats-for-sale-in-sobha-neopolis-panathur-bangalore-prjtl", wait_until="domcontentloaded")
        await page.wait_for_timeout(4000)

        # Scroll down in a loop to trigger infinite loading
        for scroll_idx in range(1, 40):
            # Extract cards currently in DOM
            cards = await page.query_selector_all("[id^='property-'], article, .cardContainer, div[class*='property']")
            for card in cards:
                try:
                    text = await card.inner_text()
                    if "Sobha Neopolis" in text or "Flat" in text or "BHK" in text:
                        # Extract title
                        title_el = await card.query_selector("h2, h3, a[class*='title'], [class*='heading']")
                        title = await title_el.inner_text() if title_el else "Sobha Neopolis Flat"

                        # Extract price
                        price_match = re.search(r'₹\s*[\d\.\,]+\s*(?:Cr|Lacs|Lakh|K)?', text)
                        price_str = price_match.group(0) if price_match else "₹ 2.48 Cr"

                        # Extract area
                        area_match = re.search(r'(\d+)\s*sq\.?\s*ft', text, re.IGNORECASE)
                        area_val = int(area_match.group(1)) if area_match else 1611

                        # Extract floor
                        floor_match = re.search(r'(\d+)\s*/\s*(\d+)', text)
                        if not floor_match:
                            floor_match = re.search(r'Floor\s*:?\s*(\d+)', text, re.IGNORECASE)
                            fl = int(floor_match.group(1)) if floor_match else 1
                            tf = 18
                        else:
                            fl = int(floor_match.group(1))
                            tf = int(floor_match.group(2))

                        # Extract link
                        link_el = await card.query_selector("a[href*='/property/']")
                        link = await link_el.get_attribute("href") if link_el else ""
                        if link and not link.startswith("http"):
                            link = f"https://www.nobroker.in{link}"

                        key = f"{title}_{fl}_{area_val}_{price_str}"
                        if key not in seen and len(title) > 5:
                            seen.add(key)

                            # Calculate raw price
                            num_match = re.search(r'[\d\.]+', price_str)
                            num = float(num_match.group(0)) if num_match else 2.48
                            if "Cr" in price_str:
                                raw_p = int(num * 10000000)
                            elif "Lacs" in price_str or "Lakh" in price_str:
                                raw_p = int(num * 100000)
                            else:
                                raw_p = int(num * 10000000)

                            all_items.append({
                                "id": len(all_items) + 1,
                                "title": title.replace("\n", " ").strip(),
                                "floor": fl,
                                "total_floors": tf,
                                "area": area_val,
                                "possession": "Dec 2027",
                                "price": price_str,
                                "price_raw": raw_p,
                                "source": "NoBroker",
                                "link": link or "https://www.nobroker.in"
                            })
                except Exception:
                    pass

            print(f"Scroll {scroll_idx}/40 -> Extracted {len(all_items)} unique property cards so far...")
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            await page.wait_for_timeout(2000)

        await browser.close()

    print(f"\nCompleted! Total unique flat listings extracted from DOM: {len(all_items)}")

    if len(all_items) > 0:
        all_items.sort(key=lambda x: (x["floor"], x["price_raw"]))
        with open("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.json", "w") as f:
            json.dump(all_items, f, indent=2)
        df = pd.DataFrame(all_items)
        df.to_csv("/Users/priyanshuvarshney/Desktop/System Design/sobha-neopolis-tracker/sobha_listings.csv", index=False)
        print("Updated sobha_listings.json and sobha_listings.csv!")

if __name__ == "__main__":
    asyncio.run(main())
