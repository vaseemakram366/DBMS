# Transaction Management Simulation


accounts = {
    "Alice": 5000,
    "Bob": 3000
}

print("Before Transaction:")
print(accounts)

amount = 1000

accounts["Alice"] -= amount
accounts["Bob"] += amount

print("\nAfter Transaction:")
print(accounts)
