# Database Crash Recovery Simulator


class CrashRecovery:
    def __init__(self, database):
        self.database = database.copy()
        self.log = []

    def write(self, transaction, key, value):
        old_value = self.database.get(key)

        self.log.append(
            ("WRITE", transaction, key, old_value, value)
        )
        self.database[key] = value

        print(f"{transaction} writes {key} = {value}")

    def commit(self, transaction):
        self.log.append(("COMMIT", transaction))
        print(f"{transaction} committed")

    def crash_and_recover(self):
        print("\nDatabase crashed!")
        print("Recovery started...")

        committed = {
            record[1]
            for record in self.log
            if record[0] == "COMMIT"
        }

        for record in self.log:
            if record[0] == "WRITE":
                _, transaction, key, old_value, new_value = record

                if transaction in committed:
                    self.database[key] = new_value

        for record in reversed(self.log):
            if record[0] == "WRITE":
                _, transaction, key, old_value, new_value = record

                if transaction not in committed:
                    if old_value is None:
                        self.database.pop(key, None)
                    else:
                        self.database[key] = old_value

        print("Recovery completed.")
        print("Final database:", self.database)


db = CrashRecovery({"A": 100, "B": 200})

db.write("T1", "A", 150)
db.commit("T1")

db.write("T2", "B", 50)

db.crash_and_recover()
