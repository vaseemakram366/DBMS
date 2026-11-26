# UNDO/REDO Recovery Simulation

database = {
    "A": 5000,
    "B": 3000
}

log = [
    {
        "account": "A",
        "old": 5000,
        "new": 7000,
        "committed": True
    },
    {
        "account": "B",
        "old": 3000,
        "new": 6000,
        "committed": False
    }
]

# Simulate database updates before crash
database["A"] = 7000
database["B"] = 6000

print("Before Recovery:", database)

# Recovery process
for record in log:
    if record["committed"]:
        # REDO committed transaction
        database[record["account"]] = record["new"]
    else:
        # UNDO uncommitted transaction
        database[record["account"]] = record["old"]

print("After Recovery:", database)
print("Recovery Completed")