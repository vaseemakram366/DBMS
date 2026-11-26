# REDO Recovery Simulation

database = {"balance": 5000}
log = []

new_value = 9000

# Record committed transaction
log.append({
    "new": new_value,
    "committed": True
})

print("Transaction Committed")

# Simulate crash before database update
print("Database Before Recovery:", database["balance"])

# REDO Recovery
for record in log:
    if record["committed"]:
        database["balance"] = record["new"]

print("REDO Applied")
print("Recovered Balance:", database["balance"])