# 📍 Area-Aware Demand Forecasting & Inventory Pre-Positioning System

![Project Dashboard](assets/dashboard_demo.png)

## 📖 Project Overview
This project is an **AI-driven logistics decision support system** designed to solve a critical e-commerce challenge: regional inventory imbalance. 

Traditional systems forecast demand globally, but this system is **Area-Aware**. It predicts **city-level product demand** by analyzing local variables like weather and festivals, then recommends **optimized inventory transfers** between regional warehouses to eliminate stockouts before they happen.

> [!IMPORTANT]
> **Why "Area-Aware"?**
> Traditional models ignore geographic context. This system uses city-specific signals (local weather, regional holidays) to detect demand "micro-climates," ensuring inventory is where the customer is, not just sitting in a central warehouse.

---

## 🏗 System Workflow
The system follows a closed-loop pipeline from raw data to a functional decision UI.

```mermaid
graph LR
    A[Data Prep] --> B[Feature Eng]
    B --> C[ML Model Selection]
    C --> D[Quantile Forecasting]
    D --> E[Regional Optimization]
    E --> F[FastAPI Dashboard]
❗ Problem StatementE-commerce platforms often suffer from improper inventory distribution due to localized demand drivers:Regional economic activitySeasonal weather patterns (e.g., heatwaves in Chennai)Local festivals (e.g., Pongal or Diwali spikes)Impact of poor distribution:Stockouts in high-demand cities.Excess Inventory (Dead stock) in low-demand regions.Increased Lead Times due to shipping from distant hubs.🛠 Features & Machine Learning Models1. Multi-Model Demand PredictionThe system evaluates multiple regressors to ensure the highest accuracy:| Model | Purpose | Strength || :--- | :--- | :--- || Linear Regression | Baseline | Interpretability || Random Forest | Non-linear capture | Handles complex feature interactions || Gradient Boosting | High Precision | Best for minimizing MAE |2. Risk-Aware Uncertainty EstimationWe utilize Quantile Regression to provide a safety buffer for planners:q10 (Pessimistic): Minimum expected demand.q50 (Median): The most likely scenario.q90 (Optimistic): Used to determine Safety Stock requirements.📊 Regional Inventory OptimizationThe system groups cities into operational hubs (e.g., Salem Region, Chennai Region) and runs a redistribution algorithm:Example Scenario:Chennai Forecast: 28 units | Salem Forecast: 72 unitsRegional Surplus/Shortage: Detection of a 25-unit gap.Recommended Action: Automate a transfer of 25 units from Chennai to Salem.Business Impact SimulationScenarioStockouts Without AIStockouts With AIEfficiency GainRegional Supply10100% Reduction🚀 Technical Stack & StructureBackend: Python, FastAPI, Scikit-learnFrontend: Jinja2, Tailwind CSS (Modern Dashboard)Data: Pandas, NumPy, MatplotlibProject StructurePlaintextAreaAwareDemandForecasting
├── data/               # Raw and processed sales datasets
├── src/
│   ├── templates/      # Modern Dashboard HTML (Tailwind CSS)
│   ├── api.py          # FastAPI Decision Engine
│   ├── train_model.py  # ML Pipeline & Quantile Regression
│   └── ...             # Optimization & Simulation scripts
└── requirements.txt
💻 Running the ProjectClone & InstallBashgit clone [https://github.com/lishanthss/area-aware-demand-forecasting.git](https://github.com/lishanthss/area-aware-demand-forecasting.git)
cd area-aware-demand-forecasting
pip install -r requirements.txt
Train the AI ModelsBashpython src/train_model.py
Launch the DashboardBashpython -m uvicorn src.api:app --reload
Access the UI at: http://127.0.0.1:8000🤝 Connect with MeInterested in AI-driven logistics or supply chain optimization? Let's connect!LinkedIn: [Your LinkedIn Profile Link]
