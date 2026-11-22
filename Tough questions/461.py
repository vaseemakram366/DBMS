# Schedule Validation Simulation


schedule = [
    ("T1", "Begin"),
    ("T2", "Begin"),
    ("T1", "Read"),
    ("T2", "Write"),
    ("T1", "Commit"),
    ("T2", "Commit")
]

active = set()
valid = True

for transaction, operation in schedule:

    if operation == "Begin":
        if transaction in active:
            valid = False
            break

        active.add(transaction)

    elif operation in ("Read", "Write"):
        if transaction not in active:
            valid = False
            break

    elif operation == "Commit":
        if transaction not in active:
            valid = False
            break

        active.remove(transaction)

if valid and not active:
    print("Valid Schedule")
else:
    print("Invalid Schedule")
