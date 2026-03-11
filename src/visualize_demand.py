import matplotlib.pyplot as plt

# Example predicted demand (replace with real predictions later if desired)
cities = ["Chennai", "Salem", "Namakkal", "Trichy"]
demand = [20.75, 71.25, 56.89, 24.77]

plt.bar(cities, demand)

plt.title("Predicted Demand by City")
plt.xlabel("City")
plt.ylabel("Units")

plt.show()