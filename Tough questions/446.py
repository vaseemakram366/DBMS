# Deadlock Detection Simulation


graph = {
    "T1": ["T2"],
    "T2": ["T3"],
    "T3": ["T1"]
}

def detect_cycle(node, visited, path):
    if node in path:
        return True

    if node in visited:
        return False

    visited.add(node)
    path.add(node)

    for neighbor in graph[node]:
        if detect_cycle(neighbor, visited, path):
            return True

    path.remove(node)
    return False


visited = set()
deadlock = False

for transaction in graph:
    if detect_cycle(transaction, visited, set()):
        deadlock = True
        break

if deadlock:
    print("Deadlock Detected!")
else:
    print("No Deadlock")
