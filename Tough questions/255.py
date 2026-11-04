# Synchronous vs Asynchronous Replication


class Replication:
    def __init__(self):
        self.primary = {}
        self.replica = {}

    def synchronous_write(self, key, value):
        self.primary[key] = value
        self.replica[key] = value

        print("Primary updated")
        print("Replica updated")
        print("Write completed after replica confirmation")

    def asynchronous_write(self, key, value):
        self.primary[key] = value

        print("Primary updated")
        print("Write completed")
        print("Replica update is pending")

    def sync_replica(self):
        self.replica = self.primary.copy()
        print("Replica synchronized")

    def show(self):
        print("Primary:", self.primary)
        print("Replica:", self.replica)


db = Replication()

print("Synchronous replication:")
db.synchronous_write(1, "Alice")
db.show()

print("\nAsynchronous replication:")
db.asynchronous_write(2, "Bob")
db.show()

db.sync_replica()
db.show()
