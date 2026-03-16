from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import pandas as pd
import os

app = FastAPI()

# Setup paths and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Load trained model and feature schema
# Ensure demand_model.pkl and feature_columns.pkl are in the same folder as this script
model = joblib.load(os.path.join(BASE_DIR, "demand_model.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "feature_columns.pkl"))

cities = ["Chennai", "Salem", "Namakkal", "Trichy"]

def predict_demand(city, product, temperature, rain, festival):
    """
    Helper function to process features and get prediction from ML model
    """
    data = {
        "temperature": float(temperature),
        "rain": float(rain),
        "is_festival": float(festival),
        f"city_{city}": 1,
        f"product_{product}": 1
    }

    df = pd.DataFrame([data])

    # Ensure feature alignment with the training schema
    for col in features:
        if col not in df.columns:
            df[col] = 0

    # Select only relevant columns in correct order
    df = df[features]

    pred = model.predict(df)[0]
    return float(round(pred, 2))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """
    Serves the landing page with the input form
    """
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.get("/decision", response_class=HTMLResponse)
async def decision(request: Request, product: str, temperature: int, rain: int, festival: int):
    """
    Core logic: Predicts demand, calculates regional totals, 
    and recommends inventory transfers.
    """
    
    # 1. Initialize and generate predictions for each city
    city_predictions = {}
    for city in cities:
        city_predictions[city] = predict_demand(city, product, temperature, rain, festival)

    # 2. Regional Demand Aggregation
    salem_region_demand = city_predictions["Salem"] + city_predictions["Namakkal"]
    chennai_region_demand = city_predictions["Chennai"] + city_predictions["Trichy"]

    # 3. Inventory Constraints (Simulated baseline stock)
    stock = {
        "Salem_region": 90,
        "Chennai_region": 90
    }

    # 4. Optimized Transfer Logic
    shortage_salem = max(0, salem_region_demand - stock["Salem_region"])
    surplus_chennai = max(0, stock["Chennai_region"] - chennai_region_demand)
    
    # The actual transfer is the smaller of what's needed vs what's available
    transfer = int(min(shortage_salem, surplus_chennai))

    # 5. Stockout Risk Simulation
    # Without AI System
    stockouts_without = 0
    if salem_region_demand > stock["Salem_region"]: stockouts_without += 1
    if chennai_region_demand > stock["Chennai_region"]: stockouts_without += 1

    # With AI-Driven Transfer
    stockouts_with = 0
    if salem_region_demand > (stock["Salem_region"] + transfer): stockouts_with += 1
    if chennai_region_demand > (stock["Chennai_region"] - transfer): stockouts_with += 1

    # 6. Bundle all data for the HTML Template
    result_data = {
        "city_predictions": city_predictions,
        "regional_demand": {
            "Salem_region": round(salem_region_demand, 2),
            "Chennai_region": round(chennai_region_demand, 2)
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

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "result": result_data
    })