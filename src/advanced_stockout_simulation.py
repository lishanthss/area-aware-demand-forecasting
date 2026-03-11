import random

regions = ["Salem_region", "Chennai_region"]

initial_stock = {
    "Salem_region": 90,
    "Chennai_region": 90
}

stockouts_without = 0
stockouts_with = 0

simulations = 1000

for _ in range(simulations):

    demand = {
        "Salem_region": random.uniform(110,140),
        "Chennai_region": random.uniform(40,70)
    }

    # scenario 1: without system
    for r in regions:
        if demand[r] > initial_stock[r]:
            stockouts_without += 1

    # scenario 2: with transfer
    transfer = 40

    new_stock = {
        "Salem_region": initial_stock["Salem_region"] + transfer,
        "Chennai_region": initial_stock["Chennai_region"] - transfer
    }

    for r in regions:
        if demand[r] > new_stock[r]:
            stockouts_with += 1

print("\nSimulation Results")
print("-------------------")

print("Stockouts without system:", stockouts_without)
print("Stockouts with system:", stockouts_with)

reduction = ((stockouts_without - stockouts_with) / stockouts_without) * 100

print("Stockout reduction:", round(reduction,2), "%")