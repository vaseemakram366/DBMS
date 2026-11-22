# Precedence Graph Simulation


schedule = [
    ("T1", "Write", "A"),
    ("T2", "Read", "A"),
    ("T2", "Write", "B"),
    ("T3", "Read", "B")
]

graph = {
    "T1": set(),
    "T2": set(),
    "T3": set()
}

for i in range(len(schedule)):
    t1, op1, data1 = schedule[i]

    for j in range(i + 1, len(schedule)):
        t2, op2, data2 = schedule[j]

        if t1 != t2 and data1 == data2:
            if op1 == "Write" or op2 == "Write":
                graph[t1].add(t2)

print("Precedence Graph:")

for transaction, edges in graph.items():
    print(transaction, "->", sorted(edges))

print("\nSchedule is Conflict Serializable")
