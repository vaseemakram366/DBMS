# Write-Ahead Logging, Analysis, REDO, and UNDO

class RecoveryManager:
    def __init__(self):
        self.log = []
        self.database = {}
        self.active = set()
        self.committed = set()

    def start_transaction(self, tid):
        self.log.append(("START", tid))
        self.active.add(tid)

    def write(self, tid, item, old_value, new_value):
        self.log.append(
            ("WRITE", tid, item, old_value, new_value)
        )

        self.database[item] = new_value

    def commit(self, tid):
        self.log.append(("COMMIT", tid))
        self.active.discard(tid)
        self.committed.add(tid)

    def show_log(self):
        print("\nLOG:")
        for i, record in enumerate(self.log):
            print(i, record)

    def show_database(self):
        print("\nDATABASE:")
        for item, value in self.database.items():
            print(item, "=", value)

    def crash(self):
        print("\n========== CRASH ==========")

        print("\nBefore Recovery:")
        self.show_database()

        self.analysis()
        self.redo()
        self.undo()

    def analysis(self):
        self.active = set()
        self.committed = set()

        for record in self.log:
            operation = record[0]
            tid = record[1]

            if operation == "START":
                self.active.add(tid)

            elif operation == "COMMIT":
                self.active.discard(tid)
                self.committed.add(tid)

        print("\nANALYSIS PHASE")
        print("Committed:", self.committed)
        print("Uncommitted:", self.active)

    def redo(self):
        print("\nREDO PHASE")

        for record in self.log:
            if record[0] == "WRITE":
                tid, item, old_value, new_value = record[1:]

                if tid in self.committed:
                    self.database[item] = new_value

                    print(
                        "REDO:",
                        tid,
                        item,
                        "->",
                        new_value
                    )

    def undo(self):
        print("\nUNDO PHASE")

        for record in reversed(self.log):
            if record[0] == "WRITE":
                tid, item, old_value, new_value = record[1:]

                if tid in self.active:
                    self.database[item] = old_value

                    print(
                        "UNDO:",
                        tid,
                        item,
                        "->",
                        old_value
                    )

        self.show_database()


db = RecoveryManager()

db.database["A"] = 100
db.database["B"] = 200

db.start_transaction("T1")
db.write("T1", "A", 100, 150)
db.write("T1", "B", 200, 250)
db.commit("T1")

db.start_transaction("T2")
db.write("T2", "A", 150, 300)
db.write("T2", "B", 250, 400)

db.show_log()

db.crash()