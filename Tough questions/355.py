# Full Database Backup Using JSON


import json

database = {
    "101": {"name": "Aman", "marks": 85},
    "102": {"name": "Rahul", "marks": 90},
    "103": {"name": "Priya", "marks": 95}
}

def create_backup(db):
    with open("backup.json", "w") as file:
        json.dump(db, file, indent=4)

    print("Full database backup saved successfully!")

create_backup(database)
