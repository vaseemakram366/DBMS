# UNDO Recovery Simulation

database = {"balance": 5000}
log = []

old_value = database["balance"]
new_value = 8000

# Store old and new values in log
log.append({"old": old_value, "new": new_value})

# Apply transaction update
database["balance"] = new_value

print("After Update:", database["balance"])

# Simulate crash before commit
print("Transaction Failed")

# UNDO Recovery
database["balance"] = log[0]["old"]

print("UNDO Applied")
print("Recovered Balance:", database["balance"])