# Incremental Backup Simulation

database = {
    "101": "Aman",
    "102": "Rahul",
    "103": "Priya"
}

# Previous full backup
backup = database.copy()

print("Previous Backup:", backup)

# Modify database
database["102"] = "Rohit"
database["104"] = "Karan"

# Track modified records
changed_records = {
    key: value
    for key, value in database.items()
    if key not in backup or backup[key] != value
}

print("Incremental Backup:", changed_records)

# Apply incremental backup
backup.update(changed_records)

print("Updated Backup:", backup)