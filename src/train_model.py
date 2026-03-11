import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error

# ---------------------------------------------
# 1. Paths
# ---------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "..", "data", "real_sales.csv")
MODEL_PATH = os.path.join(BASE_DIR, "demand_model.pkl")
FEATURES_PATH = os.path.join(BASE_DIR, "feature_columns.pkl")

# ---------------------------------------------
# 2. Load dataset
# ---------------------------------------------

print("Loading dataset...")

df = pd.read_csv(DATA_PATH)

# ---------------------------------------------
# 3. Encode categorical variables
# ---------------------------------------------

df = pd.get_dummies(df, columns=["city", "product"], drop_first=True)

# ---------------------------------------------
# 4. Create features and target
# ---------------------------------------------

X = df.drop(columns=["date", "units_sold"])
y = df["units_sold"]

# Save feature schema
joblib.dump(X.columns.tolist(), FEATURES_PATH)
print("Feature schema saved.")

# ---------------------------------------------
# 5. Train-test split
# ---------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# ---------------------------------------------
# 6. Define models
# ---------------------------------------------

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(random_state=42)
}

results = {}
trained_models = {}

print("\nTraining models for comparison...")

# ---------------------------------------------
# 7. Train and evaluate models
# ---------------------------------------------

for name, model in models.items():

    print(f"\nTraining {name}...")

    model.fit(X_train, y_train)

    preds = model.predict(X_test)

    mae = mean_absolute_error(y_test, preds)

    results[name] = mae
    trained_models[name] = model

    print(f"{name} MAE:", round(mae, 2))

# ---------------------------------------------
# 8. Select best model
# ---------------------------------------------

best_model_name = min(results, key=results.get)
best_model = trained_models[best_model_name]

print("\nModel Comparison Results")
print("------------------------")

for model_name, error in results.items():
    print(f"{model_name}: MAE = {round(error,2)}")

print("\nBest model selected:", best_model_name)

# ---------------------------------------------
# 9. Save best model
# ---------------------------------------------

joblib.dump(best_model, MODEL_PATH)

print("Model saved at:", MODEL_PATH)

# ---------------------------------------------
# 10. Train uncertainty models
# ---------------------------------------------

print("\nTraining quantile models...")

quantiles = [0.1, 0.5, 0.9]

for q in quantiles:

    model_q = GradientBoostingRegressor(
        loss="quantile",
        alpha=q,
        random_state=42
    )

    model_q.fit(X_train, y_train)

    model_path = os.path.join(BASE_DIR, f"demand_model_q{int(q*100)}.pkl")

    joblib.dump(model_q, model_path)

print("Quantile models saved successfully.")

# ---------------------------------------------
# 11. Improvement over baseline
# ---------------------------------------------

baseline_mae = results["Linear Regression"]
best_mae = results[best_model_name]

improvement = ((baseline_mae - best_mae) / baseline_mae) * 100

print("\nImprovement over baseline:", round(improvement,2), "%")