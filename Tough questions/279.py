# Distributed Backup System


class DistributedBackup:
    def __init__(self):
        self.database = {
            "Student1": "Aman",
            "Student2": "Riya",
            "Student3": "Rahul"
        }

        self.backups = {}

    def create_backup(self):
        self.backups["Server A"] = self.database.copy()
        self.backups["Server B"] = self.database.copy()

        print("Backup created on Server A")
        print("Backup created on Server B")

    def restore_backup(self, server):
        if server in self.backups:
            self.database = self.backups[server].copy()
            print("Database restored from", server)
            print("Restored Data:", self.database)
        else:
            print("Backup not available")


db = DistributedBackup()

db.create_backup()

db.database.clear()
print("\nDatabase after failure:", db.database)

db.restore_backup("Server A")
feat: implement distributed backup system