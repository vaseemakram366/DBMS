# Strict Schedule Checker


def check_strict(schedule):
    active_writers = {}
    violations = []

    for index, (transaction, operation, item) in enumerate(schedule):
        if operation in ("R", "W"):
            writer = active_writers.get(item)

            if writer is not None and writer != transaction:
                violations.append(
                    (transaction, operation, item, writer, index)
                )

            if operation == "W":
                active_writers[item] = transaction

        elif operation in ("C", "A"):
            # Release all items written by this transaction.
            items_to_release = [
                item_name
                for item_name, writer in active_writers.items()
                if writer == transaction
            ]

            for item_name in items_to_release:
                del active_writers[item_name]

    if violations:
        print("Schedule is NOT STRICT")

        for tx, op, item, writer, index in violations:
            print(
                f"{tx} performed {op}({item}) while "
                f"{writer}'s write was uncommitted "
                f"(operation {index})."
            )
    else:
        print("Schedule is STRICT")


schedule1 = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T1", "C", ""),
    ("T2", "C", "")
]

schedule2 = [
    ("T1", "W", "A"),
    ("T1", "C", ""),
    ("T2", "R", "A"),
    ("T2", "W", "A"),
    ("T2", "C", "")
]

print("Example 1:")
check_strict(schedule1)

print("\nExample 2:")
check_strict(schedule2)
