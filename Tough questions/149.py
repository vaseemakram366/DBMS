# Recoverability Checker


def check_recoverability(schedule):
    last_writer = {}
    dependencies = []
    commit_order = {}

    for index, (transaction, operation, item) in enumerate(schedule):
        if operation == "W":
            last_writer[item] = transaction

        elif operation == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != transaction:
                dependencies.append((writer, transaction))

        elif operation == "C":
            commit_order[transaction] = index

    violations = []

    for writer, reader in dependencies:
        if reader in commit_order:
            if (
                writer not in commit_order
                or commit_order[writer] > commit_order[reader]
            ):
                violations.append((writer, reader))

    if violations:
        print("Schedule is NON-RECOVERABLE")
        for writer, reader in violations:
            print(f"{reader} committed before {writer} committed.")
    else:
        print("Schedule is RECOVERABLE")


schedule1 = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T1", "C", ""),
    ("T2", "C", "")
]

schedule2 = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T2", "C", ""),
    ("T1", "C", "")
]

print("Example 1:")
check_recoverability(schedule1)

print("\nExample 2:")
check_recoverability(schedule2)
