# Transaction Log Analysis

log = [
    {"transaction": "T1", "operation": "UPDATE", "status": "COMMIT"},
    {"transaction": "T2", "operation": "UPDATE", "status": "ACTIVE"},
    {"transaction": "T3", "operation": "INSERT", "status": "COMMIT"},
    {"transaction": "T4", "operation": "DELETE", "status": "ACTIVE"}
]

committed = []
uncommitted = []

for record in log:
    if record["status"] == "COMMIT":
        committed.append(record["transaction"])
    else:
        uncommitted.append(record["transaction"])

print("Committed Transactions:", committed)
print("Uncommitted Transactions:", uncommitted)
print("Total Transactions:", len(log))