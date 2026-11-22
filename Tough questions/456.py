# Conflict Serializability Simulation


schedule = [
    ("T1", "Write", "A"),
    ("T2", "Read", "A"),
    ("T2", "Write", "B"),
    ("T1", "Read", "B")
]

graph = {
    "T1": set(),
    "T2": set()
}

for i in range(len(schedule)):
    t1, op1, data1 = schedule[i]

    for j in range(i + 1, len(schedule)):
        t2, op2, data2 = schedule[j]

        if t1 != t2 and data1 == data2:
            if op1 == "Write" or op2 == "Write":
                graph[t1].add(t2)

def has_cycle(node, visited, path):
    if node in path:
        return True

    if node in visited:
        return False

    visited.add(node)
    path.add(node)

    for neighbor in graph[node]:
        if has_cycle(neighbor, visited, path):
            return True

    path.remove(node)
    return False

visited = set()
cycle = False

for transaction in graph:
    if has_cycle(transaction, visited, set()):
        cycle = True
        break

if cycle:
    print("Not Conflict Serializable")
else:
    print("Conflict Serializable")
