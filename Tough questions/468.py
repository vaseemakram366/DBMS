# Undo and Redo Log Simulation


database = {"balance": 5000}

log = {
    "old_value": 5000,
    "new_value": 7000,
    "committed": True
}

print("Initial Balance:", database["balance"])

# Simulate a crash before the update is saved
database["balance"] = 5000

print("Database After Crash:", database["balance"])

if log["committed"]:
    database["balance"] = log["new_value"]
    print("REDO Operation Performed")
else:
    database["balance"] = log["old_value"]
    print("UNDO Operation Performed")

print("Recovered Balance:", database["balance"])
