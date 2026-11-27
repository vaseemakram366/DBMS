# Asynchronous Replication Simulation

primary_db = {"balance": 5000}
replica_db = {"balance": 5000}

# Update primary database
primary_db["balance"] = 8000

print("Primary Updated:", primary_db["balance"])
print("Replica Before Sync:", replica_db["balance"])

# Replicate changes later
replica_db.update(primary_db)

print("Replica After Sync:", replica_db["balance"])
print("Replication Completed")