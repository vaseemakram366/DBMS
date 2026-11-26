# Database Backup and Restore Simulation

import copy

database = {
    "101": "Aman",
    "102": "Rahul",
    "103": "Priya"
}

# Create backup
backup = copy.deepcopy(database)

print("Backup Created:", backup)

# Simulate data loss
database.clear()

print("After Data Loss:", database)

# Restore database
database = copy.deepcopy(backup)

print("After Restore:", database)