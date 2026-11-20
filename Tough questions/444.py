# Deadlock Simulation


transaction_1 = {"holds": "Resource A", "waiting_for": "Resource B"}
transaction_2 = {"holds": "Resource B", "waiting_for": "Resource A"}

print("Transaction 1 holds:", transaction_1["holds"])
print("Transaction 1 waits for:", transaction_1["waiting_for"])

print("\nTransaction 2 holds:", transaction_2["holds"])
print("Transaction 2 waits for:", transaction_2["waiting_for"])

if transaction_1["waiting_for"] == transaction_2["holds"] and transaction_2["waiting_for"] == transaction_1["holds"]:
    print("\nDeadlock Detected!")
else:
    print("\nNo Deadlock")
