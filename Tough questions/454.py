# Serial Schedule Simulation


schedule = [
    ("T1", "Read", "A"),
    ("T1", "Write", "A"),
    ("T1", "Commit", "-"),
    ("T2", "Read", "B"),
    ("T2", "Write", "B"),
    ("T2", "Commit", "-")
]

print("Serial Schedule:\n")

for transaction, operation, data in schedule:
    print(transaction, operation, data)

print("\nSchedule is Serial")
