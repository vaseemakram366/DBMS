# View Serializability Checker


class ViewSerializability:
    def __init__(self, schedule):
        self.schedule = schedule

    def analyze(self):
        reads = {}
        writes = {}

        for tx, op, item in self.schedule:
            if op == "R":
                reads.setdefault(item, []).append(tx)

            elif op == "W":
                writes.setdefault(item, []).append(tx)

        print("Read Operations:")

        for item, transactions in reads.items():
            print(item, ":", transactions)

        print("\nWrite Operations:")

        for item, transactions in writes.items():
            print(item, ":", transactions)

        print("\nFinal Writers:")

        for item, transactions in writes.items():
            print(item, ":", transactions[-1])

        print("\nView analysis completed.")


schedule = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T2", "W", "B"),
    ("T1", "W", "B")
]

obj = ViewSerializability(schedule)
obj.analyze()
