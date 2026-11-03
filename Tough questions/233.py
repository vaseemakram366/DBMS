# Precedence Graph Cycle Detection


def is_acyclic(graph):
    visited = set()
    active = set()

    def dfs(node):
        visited.add(node)
        active.add(node)

        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if not dfs(neighbor):
                    return False
            elif neighbor in active:
                return False

        active.remove(node)
        return True

    for node in graph:
        if node not in visited:
            if not dfs(node):
                return False

    return True


graph = {
    "T1": ["T2"],
    "T2": ["T3"],
    "T3": []
}

if is_acyclic(graph):
    print("Graph has no cycle.")
    print("Schedule is conflict-serializable.")
else:
    print("Cycle detected.")
    print("Schedule is not conflict-serializable.")
