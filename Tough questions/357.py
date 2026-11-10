# Point-in-Time Recovery Simulation


def point_in_time_recovery(initial_balance, logs, target_time):
    balance = initial_balance

    for time, operation, amount in logs:
        if time > target_time:
            break

        if operation == "deposit":
            balance += amount

        elif operation == "withdraw":
            balance -= amount

    print("Recovery time:", target_time)
    print("Recovered balance:", balance)


logs = [
    (1, "deposit", 500),
    (2, "withdraw", 200),
    (3, "deposit", 300)
]

point_in_time_recovery(1000, logs, 1)
