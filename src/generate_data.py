import os
import pandas as pd
import random
from datetime import datetime, timedelta

# -------- BASIC SETUP --------
cities = ["Coimbatore", "Madurai", "Trichy"]
products = ["Fan", "Umbrella", "Mixer Grinder"]
start_date = datetime(2024, 1, 1)
num_days = 180   # 6 months of data

data = []

# -------- DATA GENERATION --------
for city in cities:
    for product in products:
        current_date = start_date

        for _ in range(num_days):
            # Weather
            rain = random.choice([0, 1])
            temperature = random.randint(22, 38)

            # Festival logic (simple)
            is_festival = 1 if current_date.month in [1, 10] else 0

            # Base demand
            base_demand = random.randint(20, 50)

            # Product behavior
            if product == "Umbrella" and rain == 1:
                base_demand += random.randint(20, 40)

            if product == "Fan" and temperature > 30:
                base_demand += random.randint(10, 25)

            if is_festival:
                base_demand += random.randint(15, 30)

            data.append([
                current_date.strftime("%Y-%m-%d"),
                city,
                product,
                rain,
                temperature,
                is_festival,
                base_demand
            ])

            current_date += timedelta(days=1)

# -------- CREATE DATAFRAME --------
df = pd.DataFrame(data, columns=[
    "date",
    "city",
    "product",
    "rain",
    "temperature",
    "is_festival",
    "units_sold"
])

# -------- SAVE TO CSV (SAFE WAY) --------
output_dir = os.path.join("..", "data")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "sales.csv")
df.to_csv(output_path, index=False)



print("✅ Dataset created successfully!")
print("📁 File saved at:", os.path.abspath(output_path))
print(df.head())
