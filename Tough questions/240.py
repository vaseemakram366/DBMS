# Checkpoint-Based Recovery


def checkpoint_recovery(initial_db, log, checkpoint_index):
    database = initial_db.copy()
    committed = set()

    recovery_log = log[checkpoint_index:]

    for record in recovery_log:
        if record[0] == "COMMIT":
            committed.add(record[1])

    for record in recovery_log:
        if record[0] == "WRITE":
            _, transaction, key, old_value, new_value = record

            if transaction in committed:
                database[key] = new_value

    print("Recovery started from checkpoint.")

    for record in reversed(recovery_log):
        if record[0] == "WRITE":
            _, transaction, key, old_value, new_value = record

            if transaction not in committed:
                if old_value is None:
                    database.pop(key, None)
                else:
                    database[key] = old_value

    print("Recovery completed.")
    return database


database = {"A": 100, "B": 200}

log = [
    ("WRITE", "T0", "A", 100, 120),
    ("CHECKPOINT",),
    ("WRITE", "T1", "A", 120, 150),
    ("COMMIT", "T1"),
    ("WRITE", "T2", "B", 200, 50)
]

result = checkpoint_recovery(database, log, 2)
print("Recovered database:", result)
