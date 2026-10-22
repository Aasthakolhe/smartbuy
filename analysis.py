import pandas as pd
import os
import joblib

# Load trained ML artifacts
MODEL_PATH = "models/smartbuy_lgbm_model.pkl"
FEATURES_PATH = "models/model_features.pkl"

if os.path.exists(MODEL_PATH) and os.path.exists(FEATURES_PATH):
    ml_model = joblib.load(MODEL_PATH)
    feature_cols = joblib.load(FEATURES_PATH)
    print("Loaded LightGBM ML model for dynamic price predictions.")
else:
    ml_model = None


def ml_signal_for_product(category, brand, current_price, month, year=2026):
    """Predicts fair market price using LightGBM and evaluates deal quality."""
    if ml_model is None:
        # Fallback if model hasn't been trained yet
        return {"signal": "YELLOW", "predicted_fair_price": current_price}

    # Construct input feature vector
    input_data = pd.DataFrame(
        [{
            "category": category,
            "brand": brand,
            "month": month,
            "year": year,
        }]
    )

    input_encoded = pd.get_dummies(input_data)
    input_encoded = input_encoded.reindex(columns=feature_cols, fill_value=0)

    # Predict expected fair market price
    predicted_fair_price = ml_model.predict(input_encoded)[0]

    # Calculate deviation percentage
    dev_pct = (
        (current_price - predicted_fair_price) / predicted_fair_price
    ) * 100

    if dev_pct <= -5.0:
        sig = "GREEN"
        msg = f"Great deal! Current price is {abs(dev_pct):.1f}% below ML fair market baseline."
    elif dev_pct >= 5.0:
        sig = "RED"
        msg = f"Overpriced! Current price is {dev_pct:.1f}% above ML fair market baseline."
    else:
        sig = "YELLOW"
        msg = "Fair market price — no major price drop detected right now."

    return {
        "category": category,
        "brand": brand,
        "current_price": current_price,
        "predicted_fair_price": round(predicted_fair_price, 2),
        "deviation_pct": round(dev_pct, 2),
        "signal": sig,
        "message": msg,
    }