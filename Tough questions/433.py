# Transaction Log Simulation


accounts = {
    "Alice": 5000,
    "Bob": 3000
}

transaction_log = []

transaction_log.append("Transaction Started")

old_balance = accounts["Alice"]
accounts["Alice"] -= 1000

transaction_log.append(
    f"Alice: {old_balance} -> {accounts['Alice']}"
)

old_balance = accounts["Bob"]
accounts["Bob"] += 1000

transaction_log.append(
    f"Bob: {old_balance} -> {accounts['Bob']}"
)

transaction_log.append("Transaction Committed")

print("Transaction Log:")

for entry in transaction_log:
    print(entry)

print("\nFinal Accounts:")
print(accounts)
