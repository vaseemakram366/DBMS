# Cascadeless Schedule Simulation


schedule = [
    ("T1", "Write", "A"),
    ("T1", "Commit", "-"),
    ("T2", "Read", "A"),
    ("T2", "Commit", "-")
]

committed = set()
writers = {}

cascadeless = True

for transaction, operation, data in schedule:

    if operation == "Write":
        writers[data] = transaction
        print(transaction, "wrote", data)

    elif operation == "Commit":
        committed.add(transaction)
        print(transaction, "committed")

    elif operation == "Read":
        writer = writers.get(data)

        if writer is not None and writer not in committed:
            print(transaction, "read rejected")
            cascadeless = False
        else:
            print(transaction, "read", data)

if cascadeless:
    print("Cascadeless Schedule")
else:
    print("Not Cascadeless")
