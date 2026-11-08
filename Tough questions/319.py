# Immediate Database Modification


class ImmediateModification:
    def __init__(self):
        self.database = {"A": 100}
        self.log = []

    def update(self, transaction, item, new_value):
        old_value = self.database[item]

        self.log.append(
            (transaction, "UPDATE", item, old_value, new_value)
        )

        self.database[item] = new_value
        print(f"{transaction}: {item} changed {old_value} -> {new_value}")

    def commit(self, transaction):
        self.log.append(
            (transaction, "COMMIT", None, None, None)
        )
        print(f"{transaction}: COMMIT")

    def recover(self):
        committed = {
            entry[0]
            for entry in self.log
            if entry[1] == "COMMIT"
        }

        for entry in reversed(self.log):
            tx, operation, item, old_value, new_value = entry

            if operation == "UPDATE" and tx not in committed:
                self.database[item] = old_value
                print(f"UNDO {tx}: {item} restored to {old_value}")

        print("Recovered Database:", self.database)


db = ImmediateModification()

db.update("T1", "A", 200)

print("Crash Occurred!")
db.recover()
