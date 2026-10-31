# Database Write-Ahead Logging (WAL) Simulator


class WALSimulator:
    def __init__(self, initial_data):
        self.database = initial_data.copy()
        self.log = []

    def update(self, transaction, item, new_value):
        old_value = self.database[item]

        # Log the change before modifying the database.
        self.log.append({
            "transaction": transaction,
            "item": item,
            "old": old_value,
            "new": new_value,
            "committed": False
        })

        print(
            f"LOG: {transaction}, {item}: "
            f"{old_value} -> {new_value}"
        )

        self.database[item] = new_value
        print(f"Database updated: {item} = {new_value}")

    def commit(self, transaction):
        for entry in self.log:
            if entry["transaction"] == transaction:
                entry["committed"] = True

        print(f"{transaction} committed")

    def crash_recovery(self):
        print("\nCrash recovery started")

        for entry in reversed(self.log):
            if not entry["committed"]:
                self.database[entry["item"]] = entry["old"]
                print(
                    f"UNDO {entry['transaction']}: "
                    f"{entry['item']} = {entry['old']}"
                )

        for entry in self.log:
            if entry["committed"]:
                self.database[entry["item"]] = entry["new"]
                print(
                    f"REDO {entry['transaction']}: "
                    f"{entry['item']} = {entry['new']}"
                )

        print("Recovery completed")
        print("Final database:", self.database)


db = WALSimulator({"A": 100, "B": 200})

db.update("T1", "A", 150)
db.commit("T1")

db.update("T2", "B", 250)

print("\nSimulated crash!")
db.crash_recovery()
