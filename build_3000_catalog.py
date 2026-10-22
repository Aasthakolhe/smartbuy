import pandas as pd

CATEGORIES = {
    "Smartphone": ["Samsung", "Apple", "OnePlus", "Xiaomi", "Realme", "Vivo", "Oppo", "Motorola", "Nothing", "iQOO"],
    "Laptop": ["HP", "Dell", "Lenovo", "ASUS", "Acer", "MSI", "Apple", "Samsung"],
    "TV": ["Samsung", "LG", "Sony", "Mi", "TCL", "Hisense", "Vu", "OnePlus"],
    "AC": ["Voltas", "LG", "Daikin", "Samsung", "Carrier", "Hitachi", "Blue Star", "Lloyd"],
    "Refrigerator": ["Samsung", "LG", "Whirlpool", "Haier", "Godrej", "Bosch", "Hitachi"],
    "Washing Machine": ["Samsung", "LG", "IFB", "Whirlpool", "Bosch", "Godrej", "Haier"],
    "Headphones": ["boAt", "Sony", "JBL", "Sennheiser", "Bose", "Noise", "OnePlus", "Apple"],
    "Smartwatch": ["Apple", "Samsung", "Noise", "boAt", "Fire-Boltt", "Amazfit", "Garmin"],
    "Tablet": ["Samsung", "Apple", "Lenovo", "Xiaomi", "Realme", "OnePlus"],
    "Soundbar": ["Sony", "JBL", "boAt", "Samsung", "LG", "Zebronics", "Bose"],
}

products = []
pid = 1

for cat, brands in CATEGORIES.items():
    for i in range(1, 301):
        brand = brands[i % len(brands)]
        product_name = f"{brand} {cat} Series-{i} (2026 Model)"
        products.append({
            "product_id": f"PROD_{pid:04d}",
            "product": product_name,
            "category": cat,
            "brand": brand,
            "retailer": "Amazon" if pid % 2 == 0 else "Flipkart",
            "url": f"https://www.example.com/product/prod_{pid:04d}",
            "selector": ".a-price-whole" if pid % 2 == 0 else "div.Nx9qKw",
        })
        pid += 1

df = pd.DataFrame(products)
df.to_csv("data/target_3000_catalog.csv", index=False)
print(f"Created catalog with {len(df)} items in data/target_3000_catalog.csv")