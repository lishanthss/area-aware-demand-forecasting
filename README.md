# Area-Aware Demand Forecasting for E-commerce Logistics

Machine learning system that predicts product demand for different cities using contextual signals such as weather and festivals. The system also estimates uncertainty and suggests inventory placement decisions.

## Problem
E-commerce platforms often suffer from delayed deliveries due to poor inventory placement. This project forecasts demand at an area level and recommends whether to keep stock in a central warehouse or pre-position inventory in a nearby godown.

## Features
- Area-aware demand forecasting
- External signal features (weather, festival indicators)
- Uncertainty estimation using quantile regression
- Inventory decision logic
- Simulation comparing risk-aware vs basic forecasting

## Project Structure


area-aware-demand-forecasting
│
├── src
│ ├── train_model.py
│ ├── predict_demand.py
│ ├── simulation.py
│ ├── generate_data.py
│ ├── prepare_real_data.py
│ └── check_features.py
│
├── .gitignore
└── README.md

## How to Run

Train model:
python src/train_model.py

Run prediction:
python src/predict_demand.py

Run simulation:
python src/simulation.py
## System Architecture

1. Data Sources
   - Retail sales dataset
   - Weather indicators
   - Festival signals

2. Feature Engineering
   - City encoding
   - Product encoding
   - External signal features

3. Demand Forecasting Model
   - Random Forest / Gradient Boosting

4. Uncertainty Estimation
   - Quantile regression models
   - q10, q50, q90 prediction intervals

5. Decision Layer
   Inventory placement rule:
   - Pre-stock inventory in nearby warehouse
   - Keep stock in central warehouse

6. Simulation
   - Compare basic forecasting vs risk-aware forecasting

## Results

Baseline forecasting stockout rate: **49.46%**

Risk-aware forecasting stockout rate: **9.66%**

Stockout reduction: **~39.8%**

### Example Prediction

Demand forecast: 41 units  
Uncertainty range: 24 – 61 units (90% CI)

Decision:
Keep stock in central warehouse

## Data Sources

The project uses a retail sales dataset combined with contextual signals:

Retail sales dataset (city-level demand)
Weather indicators (rain, temperature features)
Festival signals (binary event indicators)


## Technologies

Python  
Pandas  
Scikit-learn  
Joblib  
Machine Learning Models:
- Random Forest
- Gradient Boosting

## Notes
Large datasets and trained models are excluded from the repository using `.gitignore`.
