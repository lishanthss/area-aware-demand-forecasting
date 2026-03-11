from fastapi import FastAPI
import joblib
import pandas as pd
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load trained model and feature schema
model = joblib.load(os.path.join(BASE_DIR, "demand_model.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "feature_columns.pkl"))

cities = ["Chennai", "Salem", "Namakkal", "Trichy"]


def predict(city, product, temperature, rain, festival):

    data = {
        "temperature": temperature,
        "rain": rain,
        "is_festival": festival,
        f"city_{city}": 1,
        f"product_{product}": 1
    }

    df = pd.DataFrame([data])

    # Ensure feature alignment
    for col in features:
        if col not in df.columns:
            df[col] = 0

    df = df[features]

    pred = model.predict(df)[0]

    return float(round(pred, 2))


@app.get("/decision")
def decision(product: str, temperature: int, rain: int, festival: int):

    city_predictions = {}

    # Predict demand for each city
    for city in cities:
        city_predictions[city] = predict(city, product, temperature, rain, festival)

    # Regional demand
    salem_region = city_predictions["Salem"] + city_predictions["Namakkal"]
    chennai_region = city_predictions["Chennai"] + city_predictions["Trichy"]

    # -----------------------------
    # Current stock levels
    # -----------------------------
    stock = {
        "Salem_region": 90,
        "Chennai_region": 90
    }

    # -----------------------------
    # Safe transfer logic
    # -----------------------------
    # current stock
    stock = {
        "Salem_region": 90,
        "Chennai_region": 90
    }

    # shortage in Salem region
    shortage = max(0, salem_region - stock["Salem_region"])

    # surplus in Chennai region
    surplus = max(0, stock["Chennai_region"] - chennai_region)

    # optimized transfer
    transfer = int(min(shortage, surplus))

    # -----------------------------
    # Stockout simulation
    # -----------------------------

    # Without system
    stockouts_without = 0

    if salem_region > stock["Salem_region"]:
        stockouts_without += 1

    if chennai_region > stock["Chennai_region"]:
        stockouts_without += 1

    # With system
    stock_after = {
        "Salem_region": stock["Salem_region"] + transfer,
        "Chennai_region": stock["Chennai_region"] - transfer
    }

    stockouts_with = 0

    if salem_region > stock_after["Salem_region"]:
        stockouts_with += 1

    if chennai_region > stock_after["Chennai_region"]:
        stockouts_with += 1

    # -----------------------------
    # API Response
    # -----------------------------

    return {
        "city_predictions": city_predictions,
        "regional_demand": {
            "Salem_region": round(salem_region, 2),
            "Chennai_region": round(chennai_region, 2)
        },
        "recommended_transfer": {
            "from": "Chennai_region",
            "to": "Salem_region",
            "units": transfer
        },
        "stockout_analysis": {
            "without_system": stockouts_without,
            "with_system": stockouts_with
        }
    }