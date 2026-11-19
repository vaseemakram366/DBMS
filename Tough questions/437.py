# Lost Update Simulation


account = {"balance": 5000}

print("Initial Balance:", account["balance"])

transaction_1 = account["balance"]
transaction_2 = account["balance"]

transaction_1 += 1000
transaction_2 -= 500

account["balance"] = transaction_1
print("After Transaction 1:", account["balance"])

account["balance"] = transaction_2
print("After Transaction 2:", account["balance"])

print("Final Balance:", account["balance"])
