# Database Backup Using File Handling


database = {
    "101": "Aman,85",
    "102": "Rahul,90",
    "103": "Priya,95"
}

def create_backup(db):
    with open("database_backup.txt", "w") as file:
        for student_id, details in db.items():
            file.write(f"{student_id}:{details}\n")

    print("Database backup created successfully!")

create_backup(database)

with open("database_backup.txt", "r") as file:
    print("\nBackup File Content:")
    print(file.read(), end="")
