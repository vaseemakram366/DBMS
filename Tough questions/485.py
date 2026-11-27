# Master-Slave Replication

master_db = {
    "101": "Aman",
    "102": "Rahul"
}

slave_db = master_db.copy()

print("Master Database:", master_db)
print("Slave Database:", slave_db)

# Write operation on Master
master_db["103"] = "Priya"

print("After Master Update:", master_db)

# Replicate changes to Slave
slave_db.update(master_db)

print("After Replication:", slave_db)

# Read operation from Slave
print("Read from Slave:", slave_db["103"])