# Dirty Read Simulation


accounts = {
    "Alice": 5000
}

print("Initial Balance:", accounts["Alice"])

transaction_1 = accounts.copy()

transaction_1["Alice"] = 3000

print("Transaction 1 Updated Balance:",
      transaction_1["Alice"])

dirty_read = transaction_1["Alice"]

print("Transaction 2 Reads:", dirty_read)

transaction_1 = accounts.copy()

print("Transaction 1 Rolled Back")

print("Actual Database Balance:",
      accounts["Alice"])

print("Dirty Read Value:", dirty_read)
