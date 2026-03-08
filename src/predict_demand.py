import pandas as pd
import joblib
import os

# Base directory = src
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load feature schema
FEATURES_PATH = os.path.join(BASE_DIR, "feature_columns.pkl")
training_columns = joblib.load(FEATURES_PATH)
# Paths
MODEL_PATH = os.path.join(BASE_DIR, "demand_model.pkl")
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "real_sales.csv")

# Load model
model = joblib.load(MODEL_PATH)
# Load quantile models (for uncertainty)
model_q10 = joblib.load(os.path.join(BASE_DIR, "demand_model_q10.pkl"))
model_q50 = joblib.load(os.path.join(BASE_DIR, "demand_model_q50.pkl"))
model_q90 = joblib.load(os.path.join(BASE_DIR, "demand_model_q90.pkl"))


# Example future input
new_input = {
    "rain": 1,
    "temperature": 32,
    "is_festival": 1,
    "city_Trichy": 1,
    "product_Fan": 1
}

input_df = pd.DataFrame([new_input])

# Align input with training feature schema
for col in training_columns:
    if col not in input_df.columns:
        input_df[col] = 0

# Ensure correct column order
input_df = input_df[training_columns]

# Predict
# Use quantile models for uncertainty
low = model_q10.predict(input_df)[0]
mid = model_q50.predict(input_df)[0]
high = model_q90.predict(input_df)[0]

print(f"📦 Demand forecast: {round(mid)} units")
print(f"📊 Uncertainty range: {round(low)} – {round(high)} units (90% CI)")


# Inventory decision
THRESHOLD = 150
if high > THRESHOLD:
    print("🚚 Action: Pre-stock product in nearby godown")
else:
    print("🏬 Action: Keep stock in central warehouse")
