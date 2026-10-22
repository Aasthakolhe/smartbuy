"""
SmartBuy - Step 1: build a 320-product electronics catalog + monthly price history.

IMPORTANT (say this plainly in your report/viva):
- Products are REPRESENTATIVE CONFIGURATIONS (brand + typical spec tier), not
  specific tracked listings. Prices are SYNTHETIC.
- Monthly prices = base price x category seasonal pattern (category_seasonal_patterns.csv,
  my calibrated assumptions) x product-level variation + slow price trend + random
  flash-sale dips + noise + real sale-event months (festival_calendar.csv).
- The 8 real phone prices in real_prices.csv are the only real market data and are
  used separately to sanity-check the model.
"""
import pandas as pd
import numpy as np

rng = np.random.default_rng(42)
N_PER_CAT = 32
MONTHS = pd.date_range("2023-01-01", "2026-10-01", freq="MS")

# (variant label, (min price, max price)); only = brands restricted to some variant indices
CATS = {
 "Smartphone": dict(code="SP", trend=(-0.6, 0.0),
   brands=["Samsung","Apple","OnePlus","Xiaomi","Redmi","Realme","Vivo","Oppo","Motorola","Nothing","iQOO","Poco"],
   variants=[("Budget 5G 6GB/128GB",(9000,14000)),("Mid-range 5G 8GB/128GB",(16000,26000)),
             ("Mid-range 5G 8GB/256GB",(24000,34000)),("Upper-mid 5G 12GB/256GB",(32000,48000)),
             ("Flagship 5G 12GB/256GB",(55000,90000)),("Flagship 5G 12GB/512GB",(75000,130000))],
   only={"Apple":[3,4,5],"Nothing":[1,2,3],"OnePlus":[1,2,3,4],"Samsung":[0,1,2,3,4,5]}),
 "Laptop": dict(code="LP", trend=(-0.5, 0.1),
   brands=["HP","Dell","Lenovo","ASUS","Acer","MSI","Apple","Samsung"],
   variants=[("Everyday 15.6in 8GB/512GB SSD",(30000,42000)),("Performance 15.6in 16GB/512GB SSD",(45000,65000)),
             ("Thin & Light 14in 16GB/512GB SSD",(48000,70000)),("Gaming 15.6in 16GB/1TB SSD",(75000,110000)),
             ("Creator 16in 32GB/1TB SSD",(110000,180000)),("Student 14in 8GB/256GB SSD",(20000,30000))],
   only={"Apple":[2,4],"MSI":[3,4],"Samsung":[1,2,4]}),
 "TV": dict(code="TV", trend=(-0.5, 0.0),
   brands=["Samsung","LG","Sony","Mi","TCL","Hisense","Vu","OnePlus","Acer","Panasonic"],
   variants=[("32-inch HD Smart TV",(9000,15000)),("43-inch Full HD Smart TV",(18000,28000)),
             ("43-inch 4K Smart TV",(24000,38000)),("55-inch 4K Smart TV",(36000,60000)),
             ("55-inch QLED 4K Smart TV",(50000,90000)),("65-inch 4K QLED Smart TV",(70000,150000)),
             ("75-inch 4K Smart TV",(110000,250000))],
   only={"Sony":[1,3,4,5,6],"Panasonic":[1,2,3],"Vu":[0,1,2,3,4]}),
 "AC": dict(code="AC", trend=(-0.2, 0.3),
   brands=["Voltas","LG","Daikin","Samsung","Carrier","Hitachi","Blue Star","Lloyd","Panasonic","Whirlpool"],
   variants=[("1 Ton 3 Star Inverter Split AC",(30000,38000)),("1.5 Ton 3 Star Inverter Split AC",(34000,46000)),
             ("1.5 Ton 5 Star Inverter Split AC",(40000,58000)),("1.5 Ton 3 Star Window AC",(28000,36000)),
             ("2 Ton 3 Star Inverter Split AC",(46000,62000)),("1 Ton 5 Star Inverter Split AC",(36000,50000))],
   only={}),
 "Refrigerator": dict(code="RF", trend=(-0.2, 0.3),
   brands=["Samsung","LG","Whirlpool","Haier","Godrej","Bosch","Panasonic","Hitachi"],
   variants=[("190L Single Door 3 Star",(13000,18000)),("236L Double Door 3 Star",(22000,30000)),
             ("253L Double Door Inverter 3 Star",(25000,34000)),("340L Frost Free Double Door",(34000,48000)),
             ("580L Side-by-Side",(65000,110000)),("300L Convertible Double Door",(30000,42000))],
   only={"Bosch":[3,4],"Hitachi":[3,4,5]}),
 "Washing Machine": dict(code="WM", trend=(-0.2, 0.3),
   brands=["Samsung","LG","IFB","Whirlpool","Bosch","Godrej","Haier","Panasonic"],
   variants=[("6.5kg Semi-Automatic Top Load",(9000,14000)),("7kg Fully Automatic Top Load",(15000,24000)),
             ("8kg Fully Automatic Top Load",(20000,30000)),("7kg Front Load Inverter",(24000,34000)),
             ("8kg Front Load Inverter",(28000,42000)),("9kg Front Load with Steam",(36000,60000))],
   only={"Bosch":[3,4,5],"IFB":[1,2,3,4,5]}),
 "Headphones": dict(code="HP", trend=(-0.4, 0.0),
   brands=["boAt","Sony","JBL","Sennheiser","Bose","Noise","OnePlus","Apple","Samsung","Realme"],
   variants=[("True Wireless Earbuds",(1500,4000)),("Neckband Bluetooth Earphones",(1000,2500)),
             ("Over-ear Wireless Headphones",(3000,9000)),("ANC True Wireless Earbuds",(5000,14000)),
             ("Premium ANC Over-ear Headphones",(18000,38000))],
   only={"Apple":[3,4],"Sennheiser":[2,3,4],"Bose":[3,4],"boAt":[0,1,2],"Noise":[0,1,2],"Realme":[0,1,2,3]}),
 "Smartwatch": dict(code="SW", trend=(-0.5, 0.0),
   brands=["Apple","Samsung","Noise","boAt","Fire-Boltt","Amazfit","Garmin","Fitbit","OnePlus","Realme","Huawei","Xiaomi","Titan","Google"],
   variants=[("Basic Fitness Smartwatch",(1200,3000)),("Calling Smartwatch AMOLED",(2500,6000)),
             ("Premium Smartwatch with GPS",(10000,25000)),("Sports GPS Watch",(15000,45000)),
             ("Fitness Band",(1500,4000))],
   only={"Apple":[2],"Samsung":[1,2,3],"Noise":[0,1,4],"boAt":[0,1,4],"Fire-Boltt":[0,1,4],"Amazfit":[1,2,3,4],
         "Garmin":[2,3],"Fitbit":[2,4],"OnePlus":[1,4],"Realme":[0,1,4],"Huawei":[1,2],"Xiaomi":[0,1,4],
         "Titan":[1,2],"Google":[2]}),
 "Tablet": dict(code="TB", trend=(-0.4, 0.0),
   brands=["Samsung","Apple","Lenovo","Xiaomi","Realme","OnePlus","Amazon","Nokia","Honor","Huawei"],
   variants=[("Entry 8-inch 3GB/32GB",(6000,10000)),("10.4-inch 4GB/64GB",(13000,22000)),
             ("11-inch 6GB/128GB",(20000,32000)),("11-inch 8GB/256GB",(30000,50000)),
             ("12.9-inch Pro 8GB/256GB",(70000,110000)),("10.1-inch 4G Calling 4GB/64GB",(11000,17000)),
             ("11-inch OLED 8GB/128GB",(35000,60000)),("Kids Edition 8-inch 2GB/32GB",(5000,9000))],
   only={"Apple":[1,2,4,6],"Amazon":[0,7],"Nokia":[0,1,7],"Realme":[1,2,5],"OnePlus":[2,3,6],"Honor":[1,2,5,6],"Huawei":[2,3]}),
 "Soundbar": dict(code="SB", trend=(-0.3, 0.0),
   brands=["Sony","JBL","boAt","Samsung","LG","Zebronics","Philips","Bose","Mi","Realme"],
   variants=[("2.0 Channel 60W Soundbar",(3000,7000)),("2.1 Channel 120W with Subwoofer",(7000,15000)),
             ("2.1 Channel 300W Dolby Audio",(14000,28000)),("3.1.2 Channel Dolby Atmos 400W",(35000,70000)),
             ("5.1 Channel 500W Home Theatre",(22000,50000))],
   only={"Bose":[3,4],"Zebronics":[0,1],"boAt":[0,1,2],"Mi":[0,1],"Realme":[0,1],"Philips":[0,1,2,4]}),
}

def rnd(x):
    step = 10 if x < 5000 else 100
    return int(round(x / step) * step)

# ---- seasonal patterns + festival months ----
pat = pd.read_csv("data/category_seasonal_patterns.csv")
seasonal = {c: g.set_index("month")["pct_deviation_from_annual_avg"].to_dict() for c, g in pat.groupby("category")}
fest = pd.read_csv("data/festival_calendar.csv", parse_dates=["start_date", "end_date"])

def festival_months(cat):
    out = set()
    for _, f in fest.iterrows():
        if f["event_name"] in ("Summer Sale", "End of Season Sale") and cat not in ("AC", "Refrigerator"):
            continue
        for p in pd.period_range(f["start_date"], f["end_date"], freq="M"):
            out.add((p.year, p.month))
    return out

catalog, history = [], []
for cat, cfg in CATS.items():
    pool = [(b, vi, 1) for b in cfg["brands"] for vi in cfg["only"].get(b, range(len(cfg["variants"])))]
    gen = 2
    while len(pool) < N_PER_CAT:                       # add "2025 model" twins if combos run short
        pool += [(b, vi, gen) for (b, vi, _) in pool[:len(pool)]]
        gen += 1
    idx = rng.permutation(len(pool))[:N_PER_CAT]
    fm = festival_months(cat)
    for n, i in enumerate(sorted(idx), 1):
        b, vi, g = pool[i]
        label, (lo, hi) = cfg["variants"][vi]
        name = f"{b} {label}" + (" (2025 model)" if g > 1 else "")
        pid = f"{cfg['code']}-{n:03d}"
        base = rnd(rng.uniform(lo, hi))
        amp = float(np.clip(rng.normal(1.0, 0.15), 0.6, 1.4))
        trend = rng.uniform(*cfg["trend"])
        catalog.append(dict(product_id=pid, product=name, category=cat, brand=b, variant=label,
                            base_price_jan2023=base, data_type="synthetic"))
        for t, d in enumerate(MONTHS):
            s = seasonal[cat][d.month] * amp
            fe = -2 if (d.year, d.month) in fm else 0
            flash = -rng.uniform(3, 8) if rng.random() < 0.06 else 0
            pct = s + fe + flash + rng.normal(0, 1.5)
            price = rnd(base * (1 + trend / 100) ** t * (1 + pct / 100))
            history.append(dict(product_id=pid, product=name, category=cat, brand=b, date=d.date(),
                                price=price, is_festival_month=int((d.year, d.month) in fm)))

cat_df = pd.DataFrame(catalog)
q = cat_df.groupby("category")["base_price_jan2023"].transform(lambda s: pd.qcut(s, 3, labels=["Budget", "Mid", "Premium"]))
cat_df["price_tier"] = q
hist_df = pd.DataFrame(history)
assert cat_df["product"].is_unique, "duplicate product names"
cat_df.to_csv("data/product_catalog.csv", index=False)
hist_df.to_csv("data/monthly_price_history.csv", index=False)
print(f"Products: {len(cat_df)} | Categories: {cat_df.category.nunique()} | Monthly rows: {len(hist_df):,}")
print(cat_df.groupby("category").size().to_string())
print(cat_df.sample(8, random_state=1)[["product_id", "product", "base_price_jan2023", "price_tier"]].to_string(index=False))
