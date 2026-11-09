# Database Checkpointing


class DatabaseCheckpoint:
    def __init__(self):
        self.database = {"A": 100, "B": 200}
        self.checkpoint = None
        self.log = []

    def update(self, item, value):
        self.log.append(("UPDATE", item, value))
        self.database[item] = value
        print(f"Updated {item} = {value}")

    def create_checkpoint(self):
        self.checkpoint = self.database.copy()
        print("Checkpoint Created:", self.checkpoint)

    def crash_recovery(self):
        self.database = self.checkpoint.copy()
        print("Database Recovered:", self.database)


db = DatabaseCheckpoint()

db.update("A", 150)
db.create_checkpoint()

db.update("B", 300)

print("Crash Occurred!")
db.crash_recovery()
