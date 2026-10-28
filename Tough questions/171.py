# Blind Write Detector


from collections import defaultdict


class BlindWriteDetector:
    def __init__(self, schedule):
        self.schedule = schedule

    def analyze(self):
        reads = defaultdict(set)
        blind_writes = []
        transaction_operations = defaultdict(list)

        # First, record every item read by each transaction.
        for transaction, operation, item in self.schedule:
            transaction_operations[transaction].append(
                (operation, item)
            )

            if operation == "R":
                reads[transaction].add(item)

        # Then identify writes without a prior read by that transaction.
        for index, (transaction, operation, item) in enumerate(
            self.schedule
        ):
            if operation != "W":
                continue

            if item not in reads[transaction]:
                blind_writes.append({
                    "transaction": transaction,
                    "item": item,
                    "position": index + 1
                })

        return blind_writes, transaction_operations

    def display(self):
        blind_writes, _ = self.analyze()

        print("Transaction Schedule:")
        for index, (transaction, operation, item) in enumerate(
            self.schedule, start=1
        ):
            print(f"{index}. T{transaction}: {operation}({item})")

        print("\nBlind Writes:")
        if not blind_writes:
            print("No blind writes found.")
        else:
            for entry in blind_writes:
                print(
                    f"T{entry['transaction']} writes "
                    f"{entry['item']} at position "
                    f"{entry['position']} without reading it."
                )

        print("\nTotal blind writes:", len(blind_writes))


if __name__ == "__main__":
    schedule = [
        (1, "W", "A"),
        (2, "R", "A"),
        (2, "W", "A"),
        (3, "R", "B"),
        (3, "W", "C"),
        (1, "W", "B"),
    ]

    detector = BlindWriteDetector(schedule)
    detector.display()
