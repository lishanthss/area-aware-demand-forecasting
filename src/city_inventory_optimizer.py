import pandas as pd

# Example predicted demand
city_demand = {
    "Chennai": 40,
    "Salem": 120,
    "Trichy": 60,
    "Namakkal": 110
}

df = pd.DataFrame(list(city_demand.items()), columns=["city", "predicted_demand"])

avg_demand = df["predicted_demand"].mean()

surplus_cities = df[df["predicted_demand"] < avg_demand]
shortage_cities = df[df["predicted_demand"] > avg_demand]

print("Average demand:", round(avg_demand))
print()

print("Surplus cities:")
print(surplus_cities)
print()

print("High demand cities:")
print(shortage_cities)
print()

for _, low in surplus_cities.iterrows():
    for _, high in shortage_cities.iterrows():

        transfer_units = int((high["predicted_demand"] - avg_demand) / 2)

        if transfer_units > 0:
            print(
                f"Move {transfer_units} units from {low['city']} warehouse to {high['city']} warehouse"
            )