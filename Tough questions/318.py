# Deferred Database Modification


class DeferredModification:
    def __init__(self):
        self.database = {"A": 100}
        self.log = []

    def update(self, transaction, item, value):
        self.log.append((transaction, "WRITE", item, value))
        print(f"{transaction}: Update logged for {item} = {value}")

    def commit(self, transaction):
        for tx, operation, item, value in self.log:
            if tx == transaction and operation == "WRITE":
                self.database[item] = value

        self.log.append((transaction, "COMMIT", None, None))
        print(f"{transaction}: COMMIT")
        print("Database:", self.database)


db = DeferredModification()

db.update("T1", "A", 200)
db.commit("T1")
