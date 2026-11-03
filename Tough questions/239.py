# Undo/Redo Logging Simulator


def recover(initial_db, log):
    database = initial_db.copy()
    committed = set()

    for record in log:
        if record[0] == "COMMIT":
            committed.add(record[1])

    print("Recovery started.")

    for record in log:
        if record[0] == "WRITE":
            _, transaction, key, old_value, new_value = record

            if transaction in committed:
                database[key] = new_value

    for record in reversed(log):
        if record[0] == "WRITE":
            _, transaction, key, old_value, new_value = record

            if transaction not in committed:
                if old_value is None:
                    database.pop(key, None)
                else:
                    database[key] = old_value

    print("Recovery completed.")
    return database


initial_db = {"A": 100, "B": 200}

log = [
    ("WRITE", "T1", "A", 100, 150),
    ("COMMIT", "T1"),
    ("WRITE", "T2", "B", 200, 50)
]

recovered_db = recover(initial_db, log)

print("Recovered database:", recovered_db)
