# Atomicity Simulation


accounts = {
    "Alice": 5000,
    "Bob": 3000
}

backup = accounts.copy()

print("Before Transaction:")
print(accounts)

try:
    accounts["Alice"] -= 1000

    raise Exception("Transaction Failed")

    accounts["Bob"] += 1000

except Exception:
    accounts = backup.copy()
    print("\nTransaction Failed!")
    print("Changes Rolled Back!")

print("\nFinal Accounts:")
print(accounts)
