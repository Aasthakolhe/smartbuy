"""
SmartBuy - validate the seasonal model against REAL tracker numbers.
Input : data/real_prices.csv (typed in by hand from public product pages)
        output/buy_wait_signals.csv (model output)
Output: output/real_validation.csv + printed comparison
"""
import pandas as pd

real = pd.read_csv("data/real_prices.csv", parse_dates=["date_checked"])
sig = pd.read_csv("output/buy_wait_signals.csv")

real["spread_pct"] = ((real.highest_price - real.lowest_price) / real.highest_price * 100).round(1)
real["above_lowest_pct"] = ((real.current_price - real.lowest_price) / real.lowest_price * 100).round(1)
real["discount_vs_mrp_pct"] = ((real.mrp - real.current_price) / real.mrp * 100).round(1)

def real_signal(p):
    # 0 = at the lowest price ever tracked, 100 = at the highest
    pos = (p.current_price - p.lowest_price) / max(p.highest_price - p.lowest_price, 1)
    return "GREEN" if pos <= 0.15 else ("RED" if pos >= 0.75 else "YELLOW")

real["real_signal"] = real.apply(real_signal, axis=1)
real["month"] = real.date_checked.dt.month
real = real.merge(sig[["category", "month", "signal"]].rename(columns={"signal": "model_signal"}),
                  on=["category", "month"], how="left")
real["match"] = real.real_signal == real.model_signal
real.to_csv("output/real_validation.csv", index=False)

print(real[["product", "current_price", "lowest_price", "highest_price",
            "above_lowest_pct", "real_signal", "model_signal", "match"]].to_string(index=False))
print(f"\nMedian real spread (high vs low): {real.spread_pct.median()}%")
print(f"Signal agreement, model vs real: {real.match.mean()*100:.0f}% of {len(real)} products")
