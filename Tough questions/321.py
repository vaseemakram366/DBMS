# Write-Ahead Logging (WAL) Simulator/


class WAL:
    def __init__(self):
        self.database = {"A": 100}
        self.log = []

    def update(self, transaction, item, new_value):
        old_value = self.database[item]

        # Log is written before database update
        self.log.append(
            (transaction, "UPDATE", item, old_value, new_value)
        )
        print("Log saved:", self.log[-1])

        self.database[item] = new_value
        print(f"Database updated: {item} = {new_value}")

    def commit(self, transaction):
        self.log.append((transaction, "COMMIT"))
        print(f"{transaction}: COMMIT")

    def recover(self):
        committed = {
            entry[0]
            for entry in self.log
            if entry[1] == "COMMIT"
        }

        for entry in reversed(self.log):
            if entry[1] == "UPDATE":
                tx, _, item, old_value, new_value = entry

                if tx in committed:
                    self.database[item] = new_value
                    print(f"REDO {tx}: {item} = {new_value}")
                else:
                    self.database[item] = old_value
                    print(f"UNDO {tx}: {item} = {old_value}")

        print("Recovered Database:", self.database)


db = WAL()

db.update("T1", "A", 200)
db.commit("T1")

db.update("T2", "A", 300)

print("Crash Occurred!")
db.recover()
