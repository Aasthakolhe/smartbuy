import os
import joblib
from lightgbm import LGBMRegressor
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

# 1. Load dataset
data_path = "data/monthly_price_history.csv"
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Could not find {data_path}.")

df = pd.read_csv(data_path, parse_dates=["date"])
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

# 2. Add product-level baseline price feature
if "product_id" in df.columns:
    df["base_level"] = df.groupby("product_id")["price"].transform("mean")
else:
    df["base_level"] = df.groupby("product")["price"].transform("mean")

features = ["category", "brand", "month", "year", "base_level"]
target = "price"

# Encode features
X = pd.get_dummies(df[features], drop_first=True)
y = df[target]

# Clean feature names to remove LightGBM whitespace warnings
X.columns = [c.replace(" ", "_") for c in X.columns]

# 3. Train / Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=42, test_size=0.2
)

# 4. Train LightGBM Model
model = LGBMRegressor(
    n_estimators=300, learning_rate=0.03, num_leaves=31, random_state=42
)
model.fit(X_train, y_train)

# 5. Evaluate Model
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("=== Optimized LightGBM Model Performance ===")
print(f"Mean Absolute Error (MAE): Rs {mae:.2f}")
print(f"R2 Score: {r2:.4f}")

# 6. Save Model
os.makedirs("models", exist_ok=True)
joblib.dump(model, "models/smartbuy_lgbm_model.pkl")
joblib.dump(X.columns.tolist(), "models/model_features.pkl")
print("Saved updated model to models/smartbuy_lgbm_model.pkl")