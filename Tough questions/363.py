# ARIES Recovery Algorithm Simulation


database = {
    "balance": 1000
}

logs = [
    ("T1", 500, "COMMIT"),
    ("T2", 200, "ACTIVE"),
    ("T3", 300, "COMMIT")
]

def aries_recovery(db, logs):

    # Phase 1: Analysis
    print("Phase 1: Analysis")

    committed = []
    active = []

    for tx, amount, status in logs:
        if status == "COMMIT":
            committed.append((tx, amount))
        else:
            active.append((tx, amount))

    print("Committed:", committed)
    print("Active:", active)

    # Phase 2: Redo
    print("\nPhase 2: Redo")

    for tx, amount in committed:
        db["balance"] += amount
        print(tx, "REDO completed")

    # Phase 3: Undo
    print("\nPhase 3: Undo")

    for tx, amount in active:
        print(tx, "UNDO completed")

    print("\nRecovery completed!")
    print("Final balance:", db["balance"])


aries_recovery(database, logs)
