# Transaction Rollback Simulation


database = {"balance": 5000}

backup = database.copy()

print("Initial Balance:", database["balance"])

database["balance"] -= 1000

print("After Transaction:", database["balance"])

choice = "ROLLBACK"

if choice == "ROLLBACK":
    database = backup.copy()
    print("Transaction Rolled Back")

print("Final Balance:", database["balance"])
