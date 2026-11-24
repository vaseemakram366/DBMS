# Savepoint and Rollback Simulation


database = {"balance": 5000}

print("Initial Balance:", database["balance"])

database["balance"] += 1000
print("After First Deposit:", database["balance"])

savepoint = database.copy()
print("Savepoint Created")

database["balance"] += 2000
print("After Second Deposit:", database["balance"])

database = savepoint.copy()
print("Rollback To Savepoint")

print("Final Balance:", database["balance"])
