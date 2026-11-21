# Optimistic Concurrency Control (OCC) Simulation


database = {"balance": 5000}
version = 1

transaction_version = version

print("Read Phase:")
print("Balance:", database["balance"])

new_balance = database["balance"] + 1000

print("\nValidation Phase:")

if transaction_version == version:
    print("Validation Successful")

    print("\nWrite Phase:")
    database["balance"] = new_balance
    version += 1

    print("Transaction Committed")
else:
    print("Transaction Aborted")

print("Final Balance:", database["balance"])
