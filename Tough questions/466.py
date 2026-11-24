# Transaction Commit Simulation


database = {"balance": 5000}

print("Initial Balance:", database["balance"])

database["balance"] += 2000

print("Updated Balance:", database["balance"])

choice = "COMMIT"

if choice == "COMMIT":
    print("Transaction Committed")
    committed_data = database.copy()

print("Saved Balance:", committed_data["balance"])
