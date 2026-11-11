# Checkpoint-Based Recovery


database = {
    "balance": 1000
}

logs = [
    ("deposit", 500),
    ("withdraw", 200),
    ("deposit", 300)
]

def checkpoint_recovery(initial_balance, logs, checkpoint_index):
    balance = initial_balance

    # Apply operations before checkpoint
    for operation, amount in logs[:checkpoint_index]:
        if operation == "deposit":
            balance += amount
        else:
            balance -= amount

    checkpoint_balance = balance
    print("Checkpoint balance:", checkpoint_balance)

    # Recover operations after checkpoint
    for operation, amount in logs[checkpoint_index:]:
        if operation == "deposit":
            balance += amount
        else:
            balance -= amount

    print("Recovered balance:", balance)


checkpoint_recovery(1000, logs, 2)
