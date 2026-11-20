# Serializable Isolation Simulation


account = {"balance": 5000}

def deposit(amount):
    account["balance"] += amount
    print("Deposited:", amount)
    print("Balance:", account["balance"])

def withdraw(amount):
    if account["balance"] >= amount:
        account["balance"] -= amount
        print("Withdrawn:", amount)
        print("Balance:", account["balance"])
    else:
        print("Insufficient Balance")

print("Initial Balance:", account["balance"])

deposit(1000)
withdraw(2000)

print("Final Balance:", account["balance"])
