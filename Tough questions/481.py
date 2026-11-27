# Full Database Backup Simulation

import copy

database = {
    "101": "Aman",
    "102": "Rahul",
    "103": "Priya",
    "104": "Karan"
}

# Create full backup
backup = copy.deepcopy(database)

print("Original Database:", database)
print("Full Backup Created:", backup)
print("Total Records Backed Up:", len(backup))

# Simulate data loss
database.clear()

# Restore full database
database = copy.deepcopy(backup)

print("Database Restored:", database)