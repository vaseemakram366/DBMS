# Distributed Checkpointing


class DistributedCheckpoint:
    def __init__(self):
        self.database = {
            "A": 100,
            "B": 200
        }
        self.checkpoint = None

    def create_checkpoint(self):
        self.checkpoint = self.database.copy()
        print("Checkpoint created:", self.checkpoint)

    def update_data(self, key, value):
        self.database[key] = value
        print("Updated database:", self.database)

    def recover(self):
        if self.checkpoint is not None:
            self.database = self.checkpoint.copy()
            print("Database recovered:", self.database)
        else:
            print("No checkpoint available")


db = DistributedCheckpoint()

db.create_checkpoint()
db.update_data("A", 500)
db.update_data("C", 300)

print("\nSystem Failure!")

db.recover()
