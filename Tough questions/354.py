# Database Backup Simulation


import copy

database = {
    "101": {"name": "Aman", "marks": 85},
    "102": {"name": "Rahul", "marks": 90},
    "103": {"name": "Priya", "marks": 95}
}

def create_backup(db):
    backup = copy.deepcopy(db)

    print("Database backup created successfully!")
    print("Backup data:", backup)

    return backup


backup_data = create_backup(database)
