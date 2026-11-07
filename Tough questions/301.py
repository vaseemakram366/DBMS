# Cascading Rollback Simulator


class CascadingRollback:
    def __init__(self):
        self.dependencies = {
            "T1": [],
            "T2": ["T1"],
            "T3": ["T2"],
            "T4": []
        }

    def rollback(self, transaction):
        aborted = set()
        stack = [transaction]

        while stack:
            current = stack.pop()

            if current in aborted:
                continue

            aborted.add(current)

            for dependent, sources in self.dependencies.items():
                if current in sources:
                    stack.append(dependent)

        print("Aborted Transactions:")

        for tx in sorted(aborted):
            print(tx)

    def run(self):
        print("Transaction T1 failed!")
        self.rollback("T1")


simulator = CascadingRollback()
simulator.run()
