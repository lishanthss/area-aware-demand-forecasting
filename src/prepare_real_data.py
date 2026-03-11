import pandas as pd
import os

# Locate project directories safely
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "train.csv")

# Load dataset
df = pd.read_csv(DATA_PATH)

print("Original dataset preview:")
print(df.head())
print("Original shape:", df.shape)


# Rename columns to match project schema
df = df.rename(columns={
    "store": "city",
    "item": "product",
    "sales": "units_sold"
})
city_mapping = {
    1: "Chennai",
    2: "Salem",
    3: "Namakkal",
    4: "Trichy",
    5: "Erode",
    6: "Madurai",
    7: "Chennai",
    8: "Salem",
    9: "Namakkal",
    10: "Trichy"
}

df["city"] = df["city"].map(city_mapping)

product_mapping = {
    1: "Fan",
    2: "AC",
    3: "Cooler",
    4: "Heater",
    5: "WashingMachine",
    6: "Refrigerator",
    7: "TV",
    8: "Mixer",
    9: "Laptop",
    10: "Mobile",
    11: "Fan",
    12: "AC",
    13: "Cooler",
    14: "Heater",
    15: "WashingMachine",
    16: "Refrigerator",
    17: "TV",
    18: "Mixer",
    19: "Laptop",
    20: "Mobile",
    21: "Fan",
    22: "AC",
    23: "Cooler",
    24: "Heater",
    25: "WashingMachine",
    26: "Refrigerator",
    27: "TV",
    28: "Mixer",
    29: "Laptop",
    30: "Mobile",
    31: "Fan",
    32: "AC",
    33: "Cooler",
    34: "Heater",
    35: "WashingMachine",
    36: "Refrigerator",
    37: "TV",
    38: "Mixer",
    39: "Laptop",
    40: "Mobile",
    41: "Fan",
    42: "AC",
    43: "Cooler",
    44: "Heater",
    45: "WashingMachine",
    46: "Refrigerator",
    47: "TV",
    48: "Mixer",
    49: "Laptop",
    50: "Mobile"
}

df["product"] = df["product"].map(product_mapping)

# Convert date
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

# Extract time features
df["month"] = df["date"].dt.month
df["day_of_week"] = df["date"].dt.dayofweek


# Simulated temperature feature
df["temperature"] = df["month"].apply(
    lambda m: 35 if m in [4,5,6] else
              30 if m in [3,7,8] else
              25
)


# Simulated rain feature
df["rain"] = df["month"].apply(
    lambda m: 1 if m in [6,7,8,9] else 0
)


# Simulated festival indicator
df["is_festival"] = df["month"].apply(
    lambda m: 1 if m in [10,11,12] else 0
)


# -------- Regional demand simulation --------

city_multiplier = {
    "Salem": 1.6,
    "Namakkal": 1.4,
    "Chennai": 1.0,
    "Trichy": 0.9,
    "Erode": 1.2,
    "Madurai": 1.1
}


def adjust_demand(row):

    demand = row["units_sold"]

    # regional economic effect
    demand = demand * city_multiplier.get(row["city"], 1)

    # product specific regional demand
    if row["product"] == "Fan" and row["city"] in ["Salem", "Namakkal"]:
        demand = demand * 1.3

    # weather effect
    if row["temperature"] > 35:
        demand = demand * 1.2

    # festival demand spike
    if row["is_festival"] == 1:
        demand = demand * 1.4

    return demand


df["units_sold"] = df.apply(adjust_demand, axis=1)


# Save processed dataset
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "data", "real_sales.csv")

df.to_csv(OUTPUT_PATH, index=False)

print("\nProcessed dataset saved successfully.")
print("Final dataset shape:", df.shape)
print("Saved at:", OUTPUT_PATH)
print("Changed dataset preview:")
print(df.head())
print("Original shape:", df.shape)