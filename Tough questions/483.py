# Differential Backup Simulation

database = {
    "101": "Aman",
    "102": "Rahul",
    "103": "Priya"
}

# Full backup
full_backup = database.copy()

print("Full Backup:", full_backup)

# First modification
database["102"] = "Rohit"

# Second modification
database["104"] = "Karan"

# Differential backup: compare with full backup
differential_backup = {
    key: value
    for key, value in database.items()
    if key not in full_backup or full_backup[key] != value
}

print("Differential Backup:", differential_backup)

# Restore using full + differential backup
restored_database = full_backup.copy()
restored_database.update(differential_backup)

print("Restored Database:", restored_database)