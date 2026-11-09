# Transaction Log Analysis


class TransactionLogAnalysis:
    def __init__(self):
        self.log = [
            ("T1", "START"),
            ("T1", "UPDATE", "A", 100, 200),
            ("T1", "COMMIT"),

            ("T2", "START"),
            ("T2", "UPDATE", "B", 300, 400),

            ("T3", "START"),
            ("T3", "UPDATE", "C", 500, 600),
            ("T3", "COMMIT")
        ]

    def analyze(self):
        committed = set()
        started = set()

        for entry in self.log:
            tx = entry[0]

            if entry[1] == "START":
                started.add(tx)

            elif entry[1] == "COMMIT":
                committed.add(tx)

        uncommitted = started - committed

        print("Committed Transactions:", sorted(committed))
        print("Uncommitted Transactions:", sorted(uncommitted))

        print("\nREDO Operations:")

        for entry in self.log:
            if entry[1] == "UPDATE" and entry[0] in committed:
                tx, _, item, old, new = entry
                print(f"REDO {tx}: {item} = {new}")

        print("\nUNDO Operations:")

        for entry in reversed(self.log):
            if entry[1] == "UPDATE" and entry[0] in uncommitted:
                tx, _, item, old, new = entry
                print(f"UNDO {tx}: {item} = {old}")


obj = TransactionLogAnalysis()
obj.analyze()
