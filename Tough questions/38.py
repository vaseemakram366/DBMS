# Write-Ahead Logging (WAL) Recovery Engine

class WALRecoveryEngine:
    def __init__(self):
        self.log = []
        self.data = {}
        self.committed = set()
        self.active = set()
        self.lsn = 0

    def write_log(self, transaction, operation, key, old_value, new_value):
        self.lsn += 1

        record = {
            "LSN": self.lsn,
            "TID": transaction,
            "operation": operation,
            "key": key,
            "old": old_value,
            "new": new_value
        }

        self.log.append(record)

        return self.lsn

    def begin(self, transaction):
        self.active.add(transaction)

        self.log.append({
            "LSN": self.lsn + 1,
            "TID": transaction,
            "operation": "BEGIN"
        })

        self.lsn += 1

    def update(self, transaction, key, value):
        old_value = self.data.get(key)

        lsn = self.write_log(
            transaction,
            "UPDATE",
            key,
            old_value,
            value
        )

        self.data[key] = value

        print(
            f"T{transaction}: "
            f"{key} = {value} "
            f"(LSN {lsn})"
        )

    def commit(self, transaction):
        self.lsn += 1

        self.log.append({
            "LSN": self.lsn,
            "TID": transaction,
            "operation": "COMMIT"
        })

        self.committed.add(transaction)
        self.active.discard(transaction)

        print(f"T{transaction} committed")

    def checkpoint(self):
        self.lsn += 1

        self.log.append({
            "LSN": self.lsn,
            "operation": "CHECKPOINT",
            "active": list(self.active)
        })

        print("CHECKPOINT created")

    def crash(self):
        print("\n*** DATABASE CRASH ***")

        self.recover()

    def recover(self):
        committed = set()
        updates = []

        for record in self.log:
            operation = record["operation"]

            if operation == "COMMIT":
                committed.add(record["TID"])

            elif operation == "UPDATE":
                updates.append(record)

        print("\nRecovery started")

        for record in reversed(updates):
            transaction = record["TID"]

            if transaction not in committed:
                key = record["key"]
                old_value = record["old"]

                if old_value is None:
                    self.data.pop(key, None)
                else:
                    self.data[key] = old_value

                print(
                    f"UNDO T{transaction}: "
                    f"{key} -> {old_value}"
                )

        print("Recovery completed")

    def show_log(self):
        print("\nWAL LOG")

        for record in self.log:
            print(record)

    def show_data(self):
        print("\nDATABASE")

        for key, value in self.data.items():
            print(f"{key} = {value}")


db = WALRecoveryEngine()

db.begin("T1")
db.update("T1", "A", 100)
db.update("T1", "B", 200)
db.commit("T1")

db.begin("T2")
db.update("T2", "A", 999)
db.update("T2", "C", 300)

db.checkpoint()

db.show_data()
db.show_log()

db.crash()

db.show_data()