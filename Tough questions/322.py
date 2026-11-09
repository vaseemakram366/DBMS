# ARIES Recovery Algorithm (Basic)


class ARIES:
    def __init__(self):
        self.database = {"A": 100}
        self.log = []

    def update(self, tx, item, new_value):
        old_value = self.database[item]

        self.log.append(
            (tx, "UPDATE", item, old_value, new_value)
        )

        self.database[item] = new_value
        print(f"{tx}: {item} = {new_value}")

    def commit(self, tx):
        self.log.append((tx, "COMMIT"))
        print(f"{tx}: COMMIT")

    def recover(self):
        print("\n--- ANALYSIS PHASE ---")

        committed = {
            entry[0]
            for entry in self.log
            if entry[1] == "COMMIT"
        }

        print("Committed:", committed)

        print("\n--- REDO PHASE ---")

        for entry in self.log:
            if entry[1] == "UPDATE":
                tx, _, item, old, new = entry

                if tx in committed:
                    self.database[item] = new
                    print(f"REDO {tx}: {item} = {new}")

        print("\n--- UNDO PHASE ---")

        for entry in reversed(self.log):
            if entry[1] == "UPDATE":
                tx, _, item, old, new = entry

                if tx not in committed:
                    self.database[item] = old
                    print(f"UNDO {tx}: {item} = {old}")

        print("\nFinal Database:", self.database)


db = ARIES()

db.update("T1", "A", 200)
db.commit("T1")

db.update("T2", "A", 300)

print("\nCrash Occurred!")
db.recover()
