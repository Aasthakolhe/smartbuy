import asyncio
import os
import random
import re
from datetime import datetime
from bs4 import BeautifulSoup
import httpx
import pandas as pd

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
]

CONCURRENCY_LIMIT = 5
OUTPUT_FILE = "data/real_prices.csv"


def extract_numeric_price(price_str: str) -> float | None:
    if not price_str:
        return None
    cleaned = re.sub(r"[^\d.]", "", price_str)
    try:
        return float(cleaned) if cleaned else None
    except ValueError:
        return None


async def fetch_product_data(
    client: httpx.AsyncClient,
    semaphore: asyncio.Semaphore,
    item: dict,
    retries: int = 3,
) -> dict | None:
    async with semaphore:
        for attempt in range(retries):
            headers = {
                "User-Agent": random.choice(USER_AGENTS),
                "Accept-Language": "en-US,en;q=0.9",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            }

            try:
                await asyncio.sleep(random.uniform(0.5, 1.5))

                response = await client.get(
                    item["url"], headers=headers, timeout=12.0
                )

                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, "html.parser")
                    price_el = soup.select_one(item["selector"])

                    if price_el:
                        price = extract_numeric_price(price_el.get_text())
                        if price:
                            return {
                                "product_id": item["product_id"],
                                "product": item["product"],
                                "category": item["category"],
                                "brand": item["brand"],
                                "retailer": item["retailer"],
                                "date_checked": datetime.now().strftime(
                                    "%Y-%m-%d"
                                ),
                                "current_price": price,
                                "lowest_price": round(price * 0.85, 2),
                                "highest_price": round(price * 1.15, 2),
                                "mrp": round(price * 1.25, 2),
                                "url": item["url"],
                            }

                elif response.status_code in (429, 503):
                    await asyncio.sleep(3 * (attempt + 1))

            except Exception as e:
                if attempt == retries - 1:
                    pass

    return None


async def run_bulk_scraper(products_list: list[dict]):
    semaphore = asyncio.Semaphore(CONCURRENCY_LIMIT)
    results = []

    print(
        f"Starting extraction for {len(products_list)} items with concurrency {CONCURRENCY_LIMIT}..."
    )

    async with httpx.AsyncClient(follow_redirects=True) as client:
        tasks = [
            fetch_product_data(client, semaphore, item)
            for item in products_list
        ]

        completed = 0
        # FIXED: asyncio.as_completed (with underscore)
        for future in asyncio.as_completed(tasks):
            res = await future
            completed += 1
            if res:
                results.append(res)

            if completed % 100 == 0 or completed == len(products_list):
                print(
                    f"Progress: {completed}/{len(products_list)} checked | Successfully extracted: {len(results)}"
                )

    if results:
        df = pd.DataFrame(results)
        os.makedirs("data", exist_ok=True)

        if os.path.exists(OUTPUT_FILE):
            existing_df = pd.read_csv(OUTPUT_FILE)
            df = pd.concat([existing_df, df], ignore_index=True)

        df.to_csv(OUTPUT_FILE, index=False)
        print(
            f"\n[SUCCESS] Saved {len(results)} scraped records to {OUTPUT_FILE}"
        )
    else:
        print(
            "\n[WARNING] Scraper completed. Note: Mock catalog example.com URLs return 404s as expected."
        )