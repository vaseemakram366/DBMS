# Recoverable Schedule Simulation


schedule = [
    ("T1", "Write", "A"),
    ("T2", "Read", "A"),
    ("T1", "Commit", "-"),
    ("T2", "Commit", "-")
]

commit_order = []
read_from = {}

for transaction, operation, data in schedule:
    if operation == "Write":
        read_from[data] = transaction

    elif operation == "Read":
        print(transaction, "reads", data, "from", read_from[data])

    elif operation == "Commit":
        commit_order.append(transaction)
        print(transaction, "committed")

t1_commit = commit_order.index("T1")
t2_commit = commit_order.index("T2")

if t1_commit < t2_commit:
    print("Recoverable Schedule")
else:
    print("Non-Recoverable Schedule")
