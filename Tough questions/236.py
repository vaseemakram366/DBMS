# Cascadeless Schedule Checker


def is_cascadeless(schedule):
    last_writer = {}
    committed = set()

    for transaction, operation, item in schedule:
        if operation == "WRITE":
            last_writer[item] = transaction

        elif operation == "READ":
            writer = last_writer.get(item)

            if writer is not None and writer != transaction:
                if writer not in committed:
                    print(
                        f"Not cascadeless: {transaction} "
                        f"reads uncommitted data from {writer}"
                    )
                    return False

        elif operation == "COMMIT":
            committed.add(transaction)

    print("Schedule is cascadeless.")
    return True


schedule = [
    ("T1", "WRITE", "A"),
    ("T1", "COMMIT", ""),
    ("T2", "READ", "A"),
    ("T2", "COMMIT", "")
]

is_cascadeless(schedule)
