# Area-Aware Demand Forecasting and Inventory Pre-Positioning System

## Project Overview

This project builds an **AI-driven logistics decision support system** for e-commerce inventory management.

Instead of forecasting demand for an entire region, the system predicts **city-level product demand** and recommends **inventory transfers between regional warehouses** to reduce stockouts and improve delivery efficiency.

The project demonstrates how **machine learning predictions can be integrated with logistics decision-making**.

---

# Problem Statement

E-commerce platforms often maintain centralized inventory in warehouses. However, product demand varies significantly across cities due to:

- regional economic activity
- seasonal weather
- festivals and holidays
- consumer purchasing patterns

Improper inventory distribution leads to:

• Stockouts in high-demand regions  
• Excess inventory in low-demand regions  
• Increased delivery delays  

This project proposes a system that:

1. Predicts **city-level product demand**
2. Aggregates demand at the **regional level**
3. Recommends **inventory transfers between warehouses**
4. Evaluates **stockout risk reduction**

---

# System Workflow


Dataset Preparation
↓
Feature Engineering
↓
Model Training & Comparison
↓
City-Level Demand Prediction
↓
Regional Demand Aggregation
↓
Inventory Transfer Recommendation
↓
Stockout Risk Simulation
↓
FastAPI Decision Service


---

# Dataset Preparation

The system uses a retail demand dataset and converts it into a **logistics forecasting dataset**.

### Original dataset fields

- date
- store
- item
- sales

### Processed dataset features

- city
- product
- units_sold
- month
- day_of_week
- temperature
- rain
- is_festival

Additional contextual signals simulate real-world demand drivers such as:

• seasonal weather conditions  
• festival demand spikes  
• regional economic patterns  

---

# Machine Learning Models

The project compares multiple regression models to select the best demand predictor.

| Model | Purpose |
|------|------|
| Linear Regression | baseline model |
| Random Forest | captures non-linear demand patterns |
| Gradient Boosting | improves prediction accuracy |

### Evaluation Metric

Mean Absolute Error (MAE)

The best-performing model is automatically selected after training.

---

# Uncertainty Estimation

To account for demand variability, the system also trains **quantile regression models**.

Models trained:

- 10th percentile model
- 50th percentile model
- 90th percentile model

Example prediction:


Predicted Demand: 80 units
Uncertainty Range: 60 – 110 units


This helps planners prepare for demand fluctuations.

---

# Regional Inventory Optimization

Cities are grouped into regions:

### Salem Region
- Salem
- Namakkal

### Chennai Region
- Chennai
- Trichy

The system:

1. predicts demand for each city
2. aggregates regional demand
3. detects shortage and surplus
4. recommends a **safe inventory transfer**

Example:


City Demand Forecast

Chennai : 28 units
Salem : 72 units
Namakkal : 56 units
Trichy : 35 units

Regional Demand

Salem Region : 128 units
Chennai Region : 64 units

Recommended Action

Move 25 units from Chennai warehouse to Salem warehouse


---

# Stockout Risk Simulation

To evaluate the inventory decision, the system simulates two scenarios.

### Scenario 1 — Without system

No inventory redistribution.

### Scenario 2 — With ML-based redistribution

Inventory is transferred between warehouses.

Example result:


Stockouts without system : 1
Stockouts with system : 0


This demonstrates how **inventory repositioning can reduce stockout risk**.

---

# API Deployment

The project exposes a **FastAPI service** to generate predictions and inventory decisions.

### Endpoint


/decision


### Example Request


/decision?product=Fan&temperature=32&rain=0&festival=1


### Example Response

```json
{
  "city_predictions": {
    "Chennai": 28.52,
    "Salem": 72,
    "Namakkal": 56.81,
    "Trichy": 35.59
  },
  "regional_demand": {
    "Salem_region": 128.81,
    "Chennai_region": 64.11
  },
  "recommended_transfer": {
    "from": "Chennai_region",
    "to": "Salem_region",
    "units": 25
  },
  "stockout_analysis": {
    "without_system": 1,
    "with_system": 1
  }
}
Technologies Used

Python

Scikit-learn

FastAPI

Pandas

NumPy

Matplotlib

Project Structure
AreaAwareDemandForecasting
│
├── data
│   └── real_sales.csv
│
├── src
│   ├── api.py
│   ├── prepare_real_data.py
│   ├── train_model.py
│   ├── regional_inventory_optimizer.py
│   ├── advanced_stockout_simulation.py
│   ├── stockout_simulation.py
│   └── visualize_demand.py
│
├── README.md
└── requirements.txt
