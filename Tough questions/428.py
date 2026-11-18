# ACID Properties Simulation


accounts = {
    "Alice": 5000,
    "Bob": 3000
}

backup = accounts.copy()

try:
    amount = 1000

    if accounts["Alice"] >= amount:
        accounts["Alice"] -= amount
        accounts["Bob"] += amount

    if accounts["Alice"] < 0 or accounts["Bob"] < 0:
        raise ValueError("Invalid balance")

    print("Transaction Committed!")

except Exception:
    accounts = backup.copy()
    print("Transaction Rolled Back!")

print("Final Accounts:")
print(accounts)
