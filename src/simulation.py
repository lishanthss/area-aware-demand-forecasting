import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "real_sales.csv")

# Load data
df = pd.read_csv(DATA_PATH)

# Prepare features same as training
df_encoded = pd.get_dummies(df, columns=["city", "product"], drop_first=True)

X = df_encoded.drop(columns=["date", "units_sold"])
y = df_encoded["units_sold"]

# Load models
model_mean = joblib.load(os.path.join(BASE_DIR, "demand_model.pkl"))
model_q90 = joblib.load(os.path.join(BASE_DIR, "demand_model_q90.pkl"))
print("prediction models loaded starting evaluation...")
# Predict
mean_pred = model_mean.predict(X)
upper_pred = model_q90.predict(X)

# Simulate stockouts
stockout_basic = 0
stockout_risk = 0

for real, mean, high in zip(y, mean_pred, upper_pred):
    if real > mean:
        stockout_basic += 1
    if real > high:
        stockout_risk += 1

n = len(y)

basic_rate = stockout_basic / n * 100
risk_rate = stockout_risk / n * 100

print("Stockout rate (basic forecast):", round(basic_rate,2), "%")
print("Stockout rate (risk-aware):", round(risk_rate,2), "%")

reduction = basic_rate - risk_rate
print("Stockout reduction:", round(reduction,2), "%")