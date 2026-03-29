import random

regions = ["Salem_region", "Chennai_region"]

stockouts_without = 0
stockouts_with = 0

simulations = 1000

for _ in range(simulations):

    initial_stock = {
        "Salem_region": random.randint(50, 150),
        "Chennai_region": random.randint(50, 150)
    }

    demand = {
        "Salem_region": random.uniform(110,140),
        "Chennai_region": random.uniform(40,70)
    }

    # scenario 1: without system
    for r in regions:
        if demand[r] > initial_stock[r]:
            stockouts_without += 1

    # scenario 2: dynamic transfer logic
    salem_diff = demand["Salem_region"] - initial_stock["Salem_region"]
    chennai_diff = demand["Chennai_region"] - initial_stock["Chennai_region"]

    new_stock = {
        "Salem_region": initial_stock["Salem_region"],
        "Chennai_region": initial_stock["Chennai_region"]
    }

    if salem_diff > 0 and chennai_diff < 0:
        transfer = min(salem_diff, abs(chennai_diff))
        new_stock["Salem_region"] += transfer
        new_stock["Chennai_region"] -= transfer
    elif chennai_diff > 0 and salem_diff < 0:
        transfer = min(chennai_diff, abs(salem_diff))
        new_stock["Chennai_region"] += transfer
        new_stock["Salem_region"] -= transfer

    for r in regions:
        if demand[r] > new_stock[r]:
            stockouts_with += 1

print("\nSimulation Results")
print("-------------------")

print("Stockouts without system:", stockouts_without)
print("Stockouts with system:", stockouts_with)

reduction = ((stockouts_without - stockouts_with) / stockouts_without) * 100

print("Stockout reduction:", round(reduction,2), "%")