# Database Replication Simulation

primary_db = {
    "101": "Aman",
    "102": "Rahul",
    "103": "Priya"
}

replica_db = {}

# Replicate data
replica_db.update(primary_db)

print("Primary Database:", primary_db)
print("Replica Database:", replica_db)

# Update primary database
primary_db["104"] = "Karan"

# Synchronize replica
replica_db.update(primary_db)

print("After Synchronization:")
print("Primary Database:", primary_db)
print("Replica Database:", replica_db)