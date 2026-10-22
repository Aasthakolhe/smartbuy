# SmartBuy - Optimal Purchase Timing for Electronics

Run: double-click run_all.bat (Windows) or `bash run_all.sh` (Mac/Linux).
Then import the CSVs from `output/` into Power BI.

## Data note (be upfront about this)
- Catalog of 320 products / 10 categories and their monthly prices are SYNTHETIC,
  generated from assumed seasonal patterns and real sale-event dates (festival_calendar.csv).
- data/real_prices.csv holds real prices typed in by hand from public product pages
  and is used only to sanity-check the model. Add more rows to it.
