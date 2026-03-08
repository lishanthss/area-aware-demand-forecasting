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

# Rename columns to match your pipeline
df = df.rename(columns={
    "store": "city",
    "item": "product",
    "sales": "units_sold"
})

# Convert date
df["date"] = pd.to_datetime(df["date"], dayfirst=True)

# Extract time features
df["month"] = df["date"].dt.month
df["day_of_week"] = df["date"].dt.dayofweek

# Simulated seasonal temperature feature
df["temperature"] = df["month"].apply(
    lambda m: 35 if m in [4,5,6] else
              30 if m in [3,7,8] else
              25
)

# Simulated rain feature (monsoon months)
df["rain"] = df["month"].apply(
    lambda m: 1 if m in [6,7,8,9] else 0
)

# Simulated festival indicator
df["is_festival"] = df["month"].apply(
    lambda m: 1 if m in [10,11,12] else 0
)

# Save processed dataset
OUTPUT_PATH = os.path.join(BASE_DIR, "..", "data", "real_sales.csv")

df.to_csv(OUTPUT_PATH, index=False)

print("Processed dataset saved successfully.")
print("Final dataset shape:", df.shape)
print("Saved at:", OUTPUT_PATH)