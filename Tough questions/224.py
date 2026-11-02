# Database Deadlock Detection Simulator


def detect_deadlock(graph):
    visited = set()
    active = set()

    def dfs(transaction):
        visited.add(transaction)
        active.add(transaction)

        for neighbor in graph.get(transaction, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in active:
                return True

        active.remove(transaction)
        return False

    for transaction in graph:
        if transaction not in visited:
            if dfs(transaction):
                return True

    return False


wait_for_graph = {
    "T1": ["T2"],
    "T2": ["T3"],
    "T3": ["T1"],
    "T4": []
}

if detect_deadlock(wait_for_graph):
    print("Deadlock detected!")
else:
    print("No deadlock detected.")
