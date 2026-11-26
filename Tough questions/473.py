# Deferred Database Modification

database = {"balance": 5000}
log = []

print("Initial Balance:", database["balance"])

new_balance = database["balance"] + 1000
log.append({"new_balance": new_balance})

print("Before Commit:", database["balance"])

# Commit
for record in log:
    database["balance"] = record["new_balance"]

print("After Commit:", database["balance"])
print("Transaction Committed")