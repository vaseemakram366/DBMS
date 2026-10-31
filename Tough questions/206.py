# Database Checkpoint and Crash Recovery Simulator


class CheckpointRecovery:
    def __init__(self, initial_data):
        self.database = initial_data.copy()
        self.log = []
        self.checkpoint_data = initial_data.copy()
        self.checkpoint_index = 0

    def update(self, transaction, item, value):
        self.log.append({
            "transaction": transaction,
            "item": item,
            "value": value,
            "committed": False
        })

        self.database[item] = value
        print(f"{transaction} updates {item} = {value}")

    def commit(self, transaction):
        for entry in self.log:
            if entry["transaction"] == transaction:
                entry["committed"] = True

        print(f"{transaction} committed")

    def checkpoint(self):
        self.checkpoint_data = self.database.copy()
        self.checkpoint_index = len(self.log)

        print("Checkpoint saved:", self.checkpoint_data)

    def recover(self):
        print("\nCrash detected")
        self.database = self.checkpoint_data.copy()

        print("Restored checkpoint:", self.database)

        for entry in self.log[self.checkpoint_index:]:
            if entry["committed"]:
                self.database[entry["item"]] = entry["value"]
                print(
                    f"REDO {entry['transaction']}: "
                    f"{entry['item']} = {entry['value']}"
                )

        print("Recovery completed")
        print("Final database:", self.database)


db = CheckpointRecovery({"A": 100, "B": 200})

db.update("T1", "A", 150)
db.commit("T1")

db.checkpoint()

db.update("T2", "B", 250)
db.commit("T2")

db.update("T3", "A", 300)

print("\nSimulated crash!")
db.recover()
