# Cascadeless Schedule Checker


def check_cascadeless(schedule):
    write_history = {}
    committed = set()
    violations = []

    for index, (transaction, operation, item) in enumerate(schedule):
        if operation == "W":
            write_history.setdefault(item, []).append(transaction)

        elif operation == "R":
            history = write_history.get(item, [])

            if history:
                writer = history[-1]

                if writer != transaction and writer not in committed:
                    violations.append(
                        (transaction, writer, item, index)
                    )

        elif operation == "C":
            committed.add(transaction)

        elif operation == "A":
            for data_item in write_history:
                write_history[data_item] = [
                    writer
                    for writer in write_history[data_item]
                    if writer != transaction
                ]

    if violations:
        print("Schedule is NOT CASCADELESS")

        for reader, writer, item, index in violations:
            print(
                f"{reader} read {item} before "
                f"{writer} committed (operation {index})."
            )
    else:
        print("Schedule is CASCADELESS")


schedule1 = [
    ("T1", "W", "A"),
    ("T1", "C", ""),
    ("T2", "R", "A"),
    ("T2", "C", "")
]

schedule2 = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T1", "C", ""),
    ("T2", "C", "")
]

print("Example 1:")
check_cascadeless(schedule1)

print("\nExample 2:")
check_cascadeless(schedule2)
