# ARIES Recovery Basics


def aries_recovery(initial_db, log):
    database = initial_db.copy()
    committed = set()
    transactions = set()

    # Phase 1: Analysis
    print("Phase 1: Analysis")

    for record in log:
        if record[0] == "WRITE":
            transactions.add(record[1])
        elif record[0] == "COMMIT":
            committed.add(record[1])

    print("Transactions found:", sorted(transactions))
    print("Committed:", sorted(committed))

    # Phase 2: Redo
    print("\nPhase 2: Redo")

    for record in log:
        if record[0] == "WRITE":
            _, transaction, key, old_value, new_value = record
            database[key] = new_value
            print(f"Redo {transaction}: {key} = {new_value}")

    # Phase 3: Undo
    print("\nPhase 3: Undo")

    for record in reversed(log):
        if record[0] == "WRITE":
            _, transaction, key, old_value, new_value = record

            if transaction not in committed:
                if old_value is None:
                    database.pop(key, None)
                else:
                    database[key] = old_value

                print(f"Undo {transaction}: restore {key}")

    return database


initial_db = {"A": 100, "B": 200}

log = [
    ("WRITE", "T1", "A", 100, 150),
    ("COMMIT", "T1"),
    ("WRITE", "T2", "B", 200, 50)
]

result = aries_recovery(initial_db, log)
print("\nRecovered database:", result)
