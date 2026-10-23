# View Serializability Checker


from itertools import permutations


class ViewSerializabilityChecker:
    def __init__(self, schedule):
        # Each operation: (transaction, operation, data_item)
        self.schedule = schedule
        self.transactions = sorted({
            tx for tx, op, item in schedule
        })

    def view_signature(self, schedule):
        reads_from = []
        final_writes = {}

        last_writer = {}

        for tx, op, item in schedule:
            if op == "R":
                # None means the read gets the initial value
                reads_from.append(
                    (tx, item, last_writer.get(item))
                )
            elif op == "W":
                last_writer[item] = tx
                final_writes[item] = tx

        return (
            frozenset(reads_from),
            frozenset(final_writes.items())
        )

    def check(self):
        target = self.view_signature(self.schedule)

        for order in permutations(self.transactions):
            serial_schedule = []

            # Preserve each transaction's internal operation order
            for tx in order:
                serial_schedule.extend(
                    op for op in self.schedule
                    if op[0] == tx
                )

            if self.view_signature(serial_schedule) == target:
                print("Schedule IS view-serializable")
                print("Equivalent serial order:", " -> ".join(order))
                return True

        print("Schedule is NOT view-serializable")
        return False


# Example 1: Conflict-serializable schedule
schedule1 = [
    ("T1", "W", "A"),
    ("T1", "R", "A"),
    ("T2", "W", "A")
]

print("=== Schedule 1 ===")
ViewSerializabilityChecker(schedule1).check()

# Example 2: View-serializable but not conflict-serializable
schedule2 = [
    ("T1", "W", "A"),
    ("T2", "W", "A"),
    ("T1", "W", "A")
]

print("\n=== Schedule 2 ===")
ViewSerializabilityChecker(schedule2).check()
