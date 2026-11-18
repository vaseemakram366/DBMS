# ROLLBACK Operation


accounts = {
    "Alice": 5000,
    "Bob": 3000
}

backup = accounts.copy()

print("Before Transaction:")
print(accounts)

accounts["Alice"] -= 1000
accounts["Bob"] += 1000

print("\nDuring Transaction:")
print(accounts)

accounts = backup.copy()

print("\nAfter ROLLBACK:")
print(accounts)
