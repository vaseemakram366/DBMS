# Non-Repeatable Read Simulation


accounts = {
    "Alice": 5000
}

print("Transaction 1 - First Read:")
print("Alice Balance:", accounts["Alice"])

accounts["Alice"] = 7000

print("\nTransaction 2 - Updated Balance:")
print("Alice Balance:", accounts["Alice"])

print("\nTransaction 1 - Second Read:")
print("Alice Balance:", accounts["Alice"])
