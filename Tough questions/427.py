# SAVEPOINT Operation


accounts = {
    "Alice": 5000,
    "Bob": 3000
}

print("Initial Accounts:")
print(accounts)

accounts["Alice"] -= 500
savepoint = accounts.copy()

accounts["Bob"] += 1000

print("\nAfter Second Operation:")
print(accounts)

accounts = savepoint.copy()

print("\nAfter ROLLBACK TO SAVEPOINT:")
print(accounts)
