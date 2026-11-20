# Repeatable Read Isolation Simulation


accounts = {"Alice": 5000}

transaction_1_snapshot = accounts.copy()

print("Transaction 1 - First Read:")
print("Alice Balance:", transaction_1_snapshot["Alice"])

accounts["Alice"] = 7000

print("\nTransaction 2 - Updated Database:")
print("Alice Balance:", accounts["Alice"])

print("\nTransaction 1 - Second Read:")
print("Alice Balance:", transaction_1_snapshot["Alice"])
