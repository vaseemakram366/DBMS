# View Serializability Checker


class ViewSerializabilityChecker:
    def __init__(self, schedule):
        self.schedule = schedule

    def analyze(self):
        reads_from = {}
        final_writer = {}
        transactions = set()

        # The most recent writer for each data item.
        last_writer = {}

        for index, (transaction, operation, item) in enumerate(
            self.schedule
        ):
            transactions.add(transaction)

            if operation == "R":
                if item in last_writer:
                    reads_from[(transaction, item, index)] = (
                        last_writer[item]
                    )
                else:
                    reads_from[(transaction, item, index)] = "INITIAL"

            elif operation == "W":
                last_writer[item] = transaction
                final_writer[item] = transaction

            else:
                raise ValueError(f"Invalid operation: {operation}")

        return {
            "transactions": transactions,
            "reads_from": reads_from,
            "final_writer": final_writer,
        }


def view_equivalent(schedule1, schedule2):
    if sorted(schedule1) != sorted(schedule2):
        return False, "Schedules contain different operations."

    result1 = ViewSerializabilityChecker(schedule1).analyze()
    result2 = ViewSerializabilityChecker(schedule2).analyze()

    # Match reads by their transaction and data item.
    def read_sources(schedule, result):
        sources = {}
        for (transaction, item, index), source in result[
            "reads_from"
        ].items():
            key = (transaction, item, index_by_operation(schedule, index))
            sources[key] = source
        return sources

    # Operation identity is needed when a transaction reads
    # the same item more than once.
    def indexed_reads(schedule):
        counts = {}
        reads = {}

        for transaction, operation, item in schedule:
            if operation != "R":
                continue

            key = (transaction, item)
            occurrence = counts.get(key, 0)
            counts[key] = occurrence + 1
            reads[(transaction, item, occurrence)] = None

        return reads

    def read_from_signature(schedule, result):
        counts = {}
        signature = {}

        for index, (transaction, operation, item) in enumerate(schedule):
            if operation == "R":
                key = (transaction, item)
                occurrence = counts.get(key, 0)
                counts[key] = occurrence + 1
                signature[(transaction, item, occurrence)] = (
                    result["reads_from"][(transaction, item, index)]
                )

        return signature

    reads1 = read_from_signature(schedule1, result1)
    reads2 = read_from_signature(schedule2, result2)

    if reads1 != reads2:
        return False, "Read-from relationships differ."

    if result1["final_writer"] != result2["final_writer"]:
        return False, "Final writers differ."

    return True, "Schedules are view-equivalent."


def index_by_operation(schedule, index):
    return schedule[index]


if __name__ == "__main__":
    schedule1 = [
        (1, "W", "A"),
        (2, "R", "A"),
        (2, "W", "A"),
        (3, "R", "A"),
    ]

    schedule2 = [
        (1, "W", "A"),
        (2, "R", "A"),
        (2, "W", "A"),
        (3, "R", "A"),
    ]

    equivalent, message = view_equivalent(schedule1, schedule2)

    print("Schedule 1:", schedule1)
    print("Schedule 2:", schedule2)
    print("View-equivalent:", equivalent)
    print("Result:", message)
