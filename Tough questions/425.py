# COMMIT Operation


accounts = {
    "Alice": 5000,
    "Bob": 3000
}

transaction = accounts.copy()

transaction["Alice"] -= 1000
transaction["Bob"] += 1000

accounts = transaction.copy()

print("COMMIT Successful!")
print("Updated Accounts:")
print(accounts)
