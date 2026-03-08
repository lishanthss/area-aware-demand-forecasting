import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.linear_model import LinearRegression

# 1. Load dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Build absolute path to data/sales.csv
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "real_sales.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)
# 2. Convert categorical columns (city, product)
df = pd.get_dummies(df, columns=["city", "product"], drop_first=True)
X = df.drop(columns=["date", "units_sold"])
y = df["units_sold"]
FEATURES_PATH = os.path.join(BASE_DIR, "feature_columns.pkl")
joblib.dump(X.columns.tolist(), FEATURES_PATH)

print("Feature schema saved.")

# 3. Split features and target
X = df.drop(columns=["date", "units_sold"])
y = df["units_sold"]

# 4. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print("Training Random Forest model...")

# 5. Train ML model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# -------- BASELINE MODEL --------
baseline_model = LinearRegression()
baseline_model.fit(X_train, y_train)

baseline_preds = baseline_model.predict(X_test)
baseline_mae = mean_absolute_error(y_test, baseline_preds)

print("Baseline MAE:", round(baseline_mae, 2))

# 6. Predict on test data
predictions = model.predict(X_test)

# 7. Evaluate model
mae = mean_absolute_error(y_test, predictions)

print("✅ Model trained successfully!")
print("📉 Mean Absolute Error (MAE):", round(mae, 2))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "demand_model.pkl")

joblib.dump(model, MODEL_PATH)
print("💾 Model saved at:", MODEL_PATH)

# -------- UNCERTAINTY MODELS (Quantile Regression) --------

quantiles = [0.1, 0.5, 0.9]
quantile_models = {}

for q in quantiles:
    model_q = GradientBoostingRegressor(
        loss="quantile",
        alpha=q,
        random_state=42
    )
    model_q.fit(X_train, y_train)
    quantile_models[q] = model_q

print("✅ Quantile models trained (10%, 50%, 90%)")
 # -------- SAVE QUANTILE MODELS --------
for q, model_q in quantile_models.items():
    joblib.dump(
        model_q,
        os.path.join(BASE_DIR, f"demand_model_q{int(q*100)}.pkl")
    )
improvement = ((baseline_mae - mae) / baseline_mae) * 100
print("Improvement over baseline:", round(improvement, 2), "%")
print("Quantile models saved successfully")
