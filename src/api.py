from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import joblib
import pandas as pd
import os

app = FastAPI()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Load trained model and features
model = joblib.load(os.path.join(BASE_DIR, "demand_model.pkl"))
features = joblib.load(os.path.join(BASE_DIR, "feature_columns.pkl"))

cities = ["Chennai", "Salem", "Namakkal", "Trichy"]

def predict_demand(city, product, temperature, rain, festival):
    data = {
        "temperature": float(temperature),
        "rain": float(rain),
        "is_festival": float(festival),
        f"city_{city}": 1,
        f"product_{product}": 1
    }
    df = pd.DataFrame([data])
    for col in features:
        if col not in df.columns:
            df[col] = 0
    df = df[features]
    pred = model.predict(df)[0]
    return float(round(pred, 2))

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    # Pass empty strings so the boxes start empty
    return templates.TemplateResponse(request=request, name="index.html", context={
        "request": request, 
        "result": None,
        "product": "", "temp": "", "rain": "", "fest": ""
    })

@app.get("/decision", response_class=HTMLResponse)
async def decision(request: Request, product: str, temperature: int, rain: int, festival: int):
    city_predictions = {city: predict_demand(city, product, temperature, rain, festival) for city in cities}

    salem_region = city_predictions["Salem"] + city_predictions["Namakkal"]
    chennai_region = city_predictions["Chennai"] + city_predictions["Trichy"]

    import random
    salem_stock = random.randint(80, 120)
    chennai_stock = random.randint(80, 120)

    salem_diff = salem_region - salem_stock
    chennai_diff = chennai_region - chennai_stock

    transfer = 0
    from_region = "None"
    to_region = "None"

    if salem_diff > 0 and chennai_diff < 0:
        transfer = int(min(salem_diff, abs(chennai_diff)))
        from_region = "Chennai_region"
        to_region = "Salem_region"
    elif chennai_diff > 0 and salem_diff < 0:
        transfer = int(min(chennai_diff, abs(salem_diff)))
        from_region = "Salem_region"
        to_region = "Chennai_region"

    if transfer > 0:
        if to_region == "Salem_region":
            salem_stock_with = salem_stock + transfer
            chennai_stock_with = chennai_stock - transfer
        else:
            chennai_stock_with = chennai_stock + transfer
            salem_stock_with = salem_stock - transfer
    else:
        salem_stock_with = salem_stock
        chennai_stock_with = chennai_stock

    stockouts_without = (1 if salem_region > salem_stock else 0) + (1 if chennai_region > chennai_stock else 0)
    stockouts_with = (1 if salem_region > salem_stock_with else 0) + (1 if chennai_region > chennai_stock_with else 0)

    result_data = {
        "city_predictions": city_predictions,
        "recommended_transfer": {"from": from_region, "to": to_region, "units": transfer},
        "stockout_analysis": {"without_system": stockouts_without, "with_system": stockouts_with}
    }

    # IMPORTANT: We send back the input values here
    return templates.TemplateResponse(request=request, name="index.html", context={
        "request": request, 
        "result": result_data,
        "product": product, 
        "temp": temperature, 
        "rain": rain, 
        "fest": festival
    })