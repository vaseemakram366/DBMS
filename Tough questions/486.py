# Synchronous Replication Simulation

primary_db = {"balance": 5000}
replica_db = {"balance": 5000}

new_balance = 7000

# Write on primary
primary_db["balance"] = new_balance
print("Primary Updated:", primary_db["balance"])

# Wait for replica confirmation
replica_db["balance"] = new_balance
replica_confirmed = (
    replica_db["balance"] == new_balance
)

if replica_confirmed:
    print("Replica Confirmed")
    print("Transaction Successful")
else:
    print("Transaction Failed")

print("Primary Balance:", primary_db["balance"])
print("Replica Balance:", replica_db["balance"])