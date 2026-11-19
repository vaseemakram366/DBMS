# Consistency Simulation


accounts = {
    "Alice": 5000,
    "Bob": 3000
}

amount = 6000

print("Before Transaction:")
print(accounts)

if accounts["Alice"] >= amount:
    accounts["Alice"] -= amount
    accounts["Bob"] += amount
    print("\nTransaction Successful!")
else:
    print("\nTransaction Rejected!")
    print("Insufficient Balance!")

print("\nFinal Accounts:")
print(accounts)
