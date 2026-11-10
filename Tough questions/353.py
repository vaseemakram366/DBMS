# Deadlock Detection and Recovery Combined


def has_cycle(graph):
    visited = set()
    rec_stack = set()

    def dfs(tx):
        visited.add(tx)
        rec_stack.add(tx)

        for neighbor in graph.get(tx, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(tx)
        return False

    for tx in graph:
        if tx not in visited:
            if dfs(tx):
                return True

    return False


def recover_deadlock(graph, victim):
    if has_cycle(graph):
        print("Deadlock detected!")
        print("Victim selected:", victim)

        graph.pop(victim, None)

        for tx in graph:
            graph[tx] = [
                neighbor for neighbor in graph[tx]
                if neighbor != victim
            ]

        print("Victim transaction aborted.")
        print("Updated wait-for graph:", graph)
    else:
        print("No deadlock detected.")


graph = {
    "T1": ["T2"],
    "T2": ["T3"],
    "T3": ["T1"]
}

recover_deadlock(graph, "T2")
