# Database Crash Recovery Simulation


database = {
    "balance": 1000
}

logs = [
    ("T1", 500, "COMMIT"),
    ("T2", 200, "ACTIVE"),
    ("T3", 300, "COMMIT")
]

def crash_recovery(db, transaction_logs):
    print("Database crash detected!")
    print("Starting recovery...")

    for tx, amount, status in transaction_logs:

        if status == "COMMIT":
            db["balance"] += amount
            print(f"{tx}: REDO performed")

        elif status == "ACTIVE":
            print(f"{tx}: UNDO performed")

    print("Recovery completed!")
    print("Final balance:", db["balance"])


crash_recovery(database, logs)
