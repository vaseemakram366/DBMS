# Strict Schedule Simulation


schedule = [
    ("T1", "Write", "A"),
    ("T1", "Commit", "-"),
    ("T2", "Read", "A"),
    ("T2", "Write", "A"),
    ("T2", "Commit", "-")
]

active_writers = set()
strict = True

for transaction, operation, data in schedule:

    if operation == "Write":
        if data in active_writers:
            print(transaction, "Write Rejected")
            strict = False
        else:
            active_writers.add(data)
            print(transaction, "Write", data)

    elif operation == "Read":
        if data in active_writers:
            print(transaction, "Read Rejected")
            strict = False
        else:
            print(transaction, "Read", data)

    elif operation == "Commit":
        active_writers.clear()
        print(transaction, "Committed")

if strict:
    print("Strict Schedule")
else:
    print("Not Strict")
