# Isolation Simulation



accounts = {
    "Alice": 5000,
    "Bob": 3000
}

transaction_1 = accounts.copy()
transaction_2 = accounts.copy()

transaction_1["Alice"] -= 1000
transaction_1["Bob"] += 1000

transaction_2["Alice"] -= 500
transaction_2["Bob"] += 500

print("Transaction 1:")
print(transaction_1)

print("\nTransaction 2:")
print(transaction_2)

accounts = transaction_1.copy()

print("\nCommitted Database:")
print(accounts)
