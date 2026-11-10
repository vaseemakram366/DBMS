# Transaction Log-Based Recovery


database = {
    "balance": 1000
}

transaction_log = [
    ("T1", "deposit", 500),
    ("T2", "withdraw", 200),
    ("T3", "deposit", 300)
]

def recover_database(db, logs):
    for tx, operation, amount in logs:
        if operation == "deposit":
            db["balance"] += amount

        elif operation == "withdraw":
            db["balance"] -= amount

        print(f"{tx}: {operation} {amount}")

    print("Recovered balance:", db["balance"])


recover_database(database, transaction_log)
