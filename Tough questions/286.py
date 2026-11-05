# Snapshot Isolation Simulator


class SnapshotIsolation:
    def __init__(self):
        self.database = {
            "balance": 1000
        }

    def start_transaction(self):
        snapshot = self.database.copy()
        print("Transaction started")
        print("Snapshot:", snapshot)
        return snapshot

    def update_database(self, value):
        self.database["balance"] = value
        print("Database updated:", self.database)

    def read_snapshot(self, snapshot):
        print("Transaction reads:", snapshot)


db = SnapshotIsolation()

transaction1 = db.start_transaction()

db.update_database(2000)

db.read_snapshot(transaction1)

print("Current Database:", db.database)
