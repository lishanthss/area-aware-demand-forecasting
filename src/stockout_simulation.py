import pandas as pd

# Example predicted demand from your optimizer
regional_demand = {
    "Salem_region": 128.14,
    "Chennai_region": 45.52
}

# Assume current stock levels
warehouse_stock = {
    "Salem_region": 90,
    "Chennai_region": 90
}

print("\nCURRENT STOCK LEVELS")
print("---------------------")
print(warehouse_stock)

print("\nPREDICTED DEMAND")
print("----------------")
print(regional_demand)

# -----------------------------
# Scenario 1: No reallocation
# -----------------------------

stockout_without_system = 0

for region in regional_demand:

    if regional_demand[region] > warehouse_stock[region]:
        stockout_without_system += 1

# -----------------------------
# Scenario 2: With your system
# -----------------------------

transfer = 41

warehouse_stock["Salem_region"] += transfer
warehouse_stock["Chennai_region"] -= transfer

stockout_with_system = 0

for region in regional_demand:

    if regional_demand[region] > warehouse_stock[region]:
        stockout_with_system += 1

print("\nSTOCKOUT COMPARISON")
print("--------------------")

print("Stockouts without system:", stockout_without_system)
print("Stockouts with system:", stockout_with_system)

improvement = (stockout_without_system - stockout_with_system)

print("\nStockout reduction:", improvement)