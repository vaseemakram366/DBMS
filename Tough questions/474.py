# Immediate Database Modification

database = {"balance": 5000}
log = []

old_value = database["balance"]
new_value = 7000

# Write log before database update
log.append({
    "old": old_value,
    "new": new_value,
    "committed": False
})

print("Log Written")

# Update database before commit
database["balance"] = new_value

print("Database Updated:", database["balance"])

# Simulate crash before commit
database["balance"] = log[0]["old"]

print("Crash Recovery: UNDO Applied")
print("Recovered Balance:", database["balance"])