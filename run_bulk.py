import asyncio
import pandas as pd
from bulk_scraper import run_bulk_scraper

if __name__ == "__main__":
    targets = pd.read_csv("data/target_3000_catalog.csv").to_dict(orient="records")
    asyncio.run(run_bulk_scraper(targets))