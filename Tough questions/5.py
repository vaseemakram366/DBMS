# Database Recovery — Undo/Redo

class RecoveryManager:
    def __init__(self):
        self.log = []
        self.database = {}

    def write(self, transaction, item, old, new):
        self.log.append(
            (transaction, item, old, new)
        )

        self.database[item] = new

    def commit(self, transaction):
        self.log.append(
            (transaction, "COMMIT")
        )

    def undo(self, transaction):
        print("\nUNDO:", transaction)

        for record in reversed(self.log):
            if len(record) == 4:
                t, item, old, new = record

                if t == transaction:
                    self.database[item] = old
                    print(
                        "Restored",
                        item,
                        "to",
                        old
                    )

    def show(self):
        print("\nDatabase:")
        for item, value in self.database.items():
            print(item, "=", value)


db = RecoveryManager()

db.database["A"] = 100
db.database["B"] = 200

db.write("T1", "A", 100, 150)
db.write("T1", "B", 200, 250)

db.show()

db.undo("T1")

db.show()