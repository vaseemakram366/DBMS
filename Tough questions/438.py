# Read Committed Isolation Simulation


accounts = {
    "Alice": 5000
}

transaction_1 = accounts.copy()

transaction_1["Alice"] = 3000

print("Transaction 1 - Uncommitted Update:")
print(transaction_1)

print("\nTransaction 2 - Reads Committed Data:")
print(accounts)

accounts = transaction_1.copy()

print("\nTransaction 1 - COMMIT")

print("\nTransaction 2 - Reads Again:")
print(accounts)
