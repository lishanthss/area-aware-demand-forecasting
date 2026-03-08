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
│   ├── train_model.py
│   ├── predict_demand.py
│   ├── simulation.py
│   ├── generate_data.py
│   ├── prepare_real_data.py
│   └── check_features.py
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

## Notes
Large datasets and trained models are excluded from the repository using `.gitignore`.
