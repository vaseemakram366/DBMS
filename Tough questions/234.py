# View Serializability Basics


def analyze_schedule(schedule):
    last_writer = {}
    read_from = {}
    final_writer = {}

    for transaction, operation, item in schedule:
        if operation == "READ":
            read_from[(transaction, item)] = (
                last_writer.get(item, "INITIAL")
            )

        elif operation == "WRITE":
            last_writer[item] = transaction
            final_writer[item] = transaction

    print("Read-from relationships:")

    for key, source in read_from.items():
        transaction, item = key
        print(f"{transaction} reads {item} from {source}")

    print("\nFinal writers:")

    for item, transaction in final_writer.items():
        print(f"{item}: {transaction}")


schedule = [
    ("T1", "WRITE", "A"),
    ("T2", "READ", "A"),
    ("T2", "WRITE", "A"),
    ("T1", "READ", "B"),
    ("T1", "WRITE", "B")
]

analyze_schedule(schedule)
