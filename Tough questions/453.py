# Transaction Scheduling Simulation


schedule = [
    ("T1", "Read", "A"),
    ("T2", "Read", "B"),
    ("T1", "Write", "A"),
    ("T2", "Write", "B"),
    ("T1", "Commit", "-"),
    ("T2", "Commit", "-")
]

print("Transaction Schedule:\n")

for transaction, operation, data in schedule:
    print(transaction, operation, data)

print("\nSchedule Completed")
