# Database Replication Simulator


class DatabaseReplication:
    def __init__(self):
        self.primary = {}
        self.replica1 = {}
        self.replica2 = {}

    def insert(self, key, value):
        self.primary[key] = value
        print(f"Primary updated: {key} = {value}")

    def replicate(self):
        self.replica1 = self.primary.copy()
        self.replica2 = self.primary.copy()

        print("Replication completed")

    def show_databases(self):
        print("Primary:", self.primary)
        print("Replica 1:", self.replica1)
        print("Replica 2:", self.replica2)


db = DatabaseReplication()

db.insert(1, "Alice")
db.insert(2, "Bob")

db.replicate()
db.show_databases()
