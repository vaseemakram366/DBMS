# Write-Ahead Logging (WAL) Simulation


database = {"balance": 5000}
log = []

old_value = database["balance"]
new_value = 7000

# Step 1: Write log before database update
log.append({
    "old": old_value,
    "new": new_value
})

print("Log Written:", log)

# Step 2: Update database
database["balance"] = new_value

print("Database Updated:", database["balance"])

# Step 3: Commit transaction
log.append({"status": "COMMIT"})

print("Transaction Committed")
print("Final Balance:", database["balance"])
