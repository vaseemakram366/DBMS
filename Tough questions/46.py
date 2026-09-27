# Database Checkpoint & Fuzzy Checkpoint Recovery

class CheckpointRecovery:
    def __init__(self):
        self.log = []
        self.data = {}
        self.lsn = 0

    def write_log(self, transaction, operation, key=None, old=None, new=None):
        self.lsn += 1

        record = {
            "lsn": self.lsn,
            "tid": transaction,
            "operation": operation,
            "key": key,
            "old": old,
            "new": new
        }

        self.log.append(record)

    def begin(self, tid):
        self.write_log(tid, "BEGIN")

    def update(self, tid, key, value):
        old_value = self.data.get(key)

        self.write_log(
            tid,
            "UPDATE",
            key,
            old_value,
            value
        )

        self.data[key] = value

    def commit(self, tid):
        self.write_log(tid, "COMMIT")

    def checkpoint(self):
        active = set()

        for record in self.log:
            tid = record["tid"]

            if record["operation"] == "BEGIN":
                active.add(tid)

            elif record["operation"] == "COMMIT":
                active.discard(tid)

        self.write_log(
            "SYSTEM",
            "CHECKPOINT",
            new=list(active)
        )

        print(
            f"Checkpoint created. "
            f"Active transactions: {active}"
        )

    def crash(self):
        print("\nDATABASE CRASH")

        self.recover()

    def recover(self):
        checkpoint_index = -1

        for i, record in enumerate(self.log):
            if record["operation"] == "CHECKPOINT":
                checkpoint_index = i

        committed = set()
        active = set()

        for record in self.log[checkpoint_index + 1:]:
            tid = record["tid"]
            operation = record["operation"]

            if operation == "BEGIN":
                active.add(tid)

            elif operation == "COMMIT":
                committed.add(tid)
                active.discard(tid)

        redo_transactions = committed
        undo_transactions = active

        print("\nREDO:", redo_transactions)
        print("UNDO:", undo_transactions)

        for record in self.log[checkpoint_index + 1:]:
            if (
                record["operation"] == "UPDATE"
                and record["tid"] in redo_transactions
            ):
                self.data[record["key"]] = record["new"]

                print(
                    f"REDO {record['tid']}: "
                    f"{record['key']} = {record['new']}"
                )

        for record in reversed(
            self.log[checkpoint_index + 1:]
        ):
            if (
                record["operation"] == "UPDATE"
                and record["tid"] in undo_transactions
            ):
                key = record["key"]
                old = record["old"]

                if old is None:
                    self.data.pop(key, None)
                else:
                    self.data[key] = old

                print(
                    f"UNDO {record['tid']}: "
                    f"{key} -> {old}"
                )

        print("\nRecovery completed")

    def show_log(self):
        print("\nLOG")

        for record in self.log:
            print(record)

    def show_data(self):
        print("\nDATABASE")

        print(self.data)


db = CheckpointRecovery()

db.begin("T1")
db.update("T1", "A", 100)
db.update("T1", "B", 200)
db.commit("T1")

db.begin("T2")
db.update("T2", "A", 500)

db.checkpoint()

db.begin("T3")
db.update("T3", "C", 300)
db.commit("T3")

db.begin("T4")
db.update("T4", "D", 400)

db.show_data()

db.crash()

db.show_data()