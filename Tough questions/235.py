# Recoverable Schedule Checker


def is_recoverable(schedule):
    committed = set()
    read_from = {}

    for transaction, operation, item in schedule:
        if operation == "WRITE":
            read_from[item] = transaction

        elif operation == "READ":
            writer = read_from.get(item)

            if writer is not None and writer != transaction:
                if transaction in committed:
                    print(
                        f"Non-recoverable: {transaction} "
                        f"committed before {writer}"
                    )
                    return False

        elif operation == "COMMIT":
            committed.add(transaction)

            for reader, writer in dependencies:
                if reader == transaction and writer not in committed:
                    print(
                        f"Non-recoverable: {reader} committed "
                        f"before {writer}"
                    )
                    return False

    print("Schedule is recoverable.")
    return True


dependencies = set()

def check_schedule(schedule):
    global dependencies
    dependencies = set()
    last_writer = {}

    for transaction, operation, item in schedule:
        if operation == "WRITE":
            last_writer[item] = transaction
        elif operation == "READ":
            writer = last_writer.get(item)
            if writer is not None and writer != transaction:
                dependencies.add((transaction, writer))

    return is_recoverable(schedule)


schedule = [
    ("T1", "WRITE", "A"),
    ("T2", "READ", "A"),
    ("T1", "COMMIT", ""),
    ("T2", "COMMIT", "")
]

check_schedule(schedule)
