# Database Failover Simulation

primary_db = {"balance": 7000}
replica_db = {"balance": 7000}

primary_status = "ACTIVE"
replica_status = "STANDBY"

print("Primary Status:", primary_status)
print("Replica Status:", replica_status)

# Simulate primary failure
primary_status = "FAILED"
print("Primary Database Failed")

# Failover process
if primary_status == "FAILED":
    replica_status = "ACTIVE"
    print("Failover Activated")

print("New Active Database: Replica")
print("Replica Balance:", replica_db["balance"])