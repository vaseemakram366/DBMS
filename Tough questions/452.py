# MVCC (Multi-Version Concurrency Control) Simulation


database_versions = [
    {"version": 1, "balance": 5000},
    {"version": 2, "balance": 7000}
]

transaction_1_version = 1

print("Transaction 1 reads:")
for record in database_versions:
    if record["version"] == transaction_1_version:
        print("Balance:", record["balance"])

print("\nTransaction 2 reads:")
print("Balance:", database_versions[-1]["balance"])

print("\nLatest Database Version:")
print(database_versions[-1])
