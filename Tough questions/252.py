# Incremental Database Backup


class IncrementalBackup:
    def __init__(self):
        self.database = {}
        self.last_backup = {}
        self.backup = {}

    def insert(self, key, value):
        self.database[key] = value
        print(f"Updated record {key}")

    def create_backup(self):
        changes = {
            key: value
            for key, value in self.database.items()
            if key not in self.last_backup
            or self.last_backup[key] != value
        }

        self.backup.update(changes)
        self.last_backup = self.database.copy()

        print("Incremental backup:", changes)

    def show_backup(self):
        print("Backup storage:", self.backup)


db = IncrementalBackup()

db.insert(1, "Alice")
db.insert(2, "Bob")

db.create_backup()

db.insert(2, "Bob Updated")
db.insert(3, "Charlie")

db.create_backup()
db.show_backup()
