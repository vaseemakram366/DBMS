# Database Backup and Restore Simulator


class Database:
    def __init__(self):
        self.data = {}
        self.backup_data = None

    def insert(self, key, value):
        self.data[key] = value
        print(f"Inserted: {key} = {value}")

    def create_backup(self):
        self.backup_data = self.data.copy()
        print("Backup created successfully")

    def show_data(self):
        print("Database:", self.data)

    def restore_backup(self):
        if self.backup_data is None:
            print("No backup available")
            return

        self.data = self.backup_data.copy()
        print("Database restored successfully")


db = Database()

db.insert(1, "Alice")
db.insert(2, "Bob")

db.create_backup()

db.insert(3, "Charlie")
db.show_data()

db.restore_backup()
db.show_data()
