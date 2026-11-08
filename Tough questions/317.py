# Checkpoint-Based Recovery


class CheckpointRecovery:
    def __init__(self):
        self.database = {"A": 100, "B": 200}
        self.checkpoint = None
        self.log = []

    def update(self, item, value):
        old_value = self.database[item]

        self.log.append(
            (item, old_value, value)
        )

        self.database[item] = value
        print(f"Updated {item} = {value}")

    def create_checkpoint(self):
        self.checkpoint = self.database.copy()

        print("Checkpoint Created:", self.checkpoint)

    def recover(self):
        if self.checkpoint is not None:
            self.database = self.checkpoint.copy()

        print("Database Recovered:", self.database)


db = CheckpointRecovery()

db.update("A", 150)
db.create_checkpoint()

db.update("B", 300)

print("Crash Occurred!")

db.recover()
