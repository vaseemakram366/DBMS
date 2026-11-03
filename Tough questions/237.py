# Strict Schedule Checker


def is_strict(schedule):
    active_writers = {}

    for transaction, operation, item in schedule:
        if operation in ("READ", "WRITE"):
            writer = active_writers.get(item)

            if writer is not None and writer != transaction:
                print(
                    f"Not strict: {transaction} accesses "
                    f"{item} while {writer} holds an uncommitted write"
                )
                return False

            if operation == "WRITE":
                active_writers[item] = transaction

        elif operation in ("COMMIT", "ABORT"):
            for item_name, writer in list(active_writers.items()):
                if writer == transaction:
                    del active_writers[item_name]

    print("Schedule is strict.")
    return True


schedule = [
    ("T1", "WRITE", "A"),
    ("T1", "COMMIT", ""),
    ("T2", "READ", "A"),
    ("T2", "COMMIT", "")
]

is_strict(schedule)
