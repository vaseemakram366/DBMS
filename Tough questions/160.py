# Conflict Serializability Repair Analyzer


from collections import defaultdict, deque


def build_conflict_graph(schedule):
    graph = defaultdict(set)
    edge_details = defaultdict(list)
    transactions = {tx for tx, _, _ in schedule}

    for tx in transactions:
        graph[tx]

    for i in range(len(schedule)):
        tx1, op1, item1 = schedule[i]

        if op1 not in ("R", "W"):
            continue

        for j in range(i + 1, len(schedule)):
            tx2, op2, item2 = schedule[j]

            if tx1 == tx2 or item1 != item2:
                continue

            if op2 not in ("R", "W"):
                continue

            if op1 == "W" or op2 == "W":
                graph[tx1].add(tx2)
                edge_details[(tx1, tx2)].append(
                    (i, j, item1, op1, op2)
                )

    return graph, edge_details


def find_cycle(graph):
    visited = set()
    active = set()
    parent = {}

    def dfs(node):
        visited.add(node)
        active.add(node)

        for neighbor in graph[node]:
            if neighbor not in visited:
                parent[neighbor] = node
                cycle = dfs(neighbor)

                if cycle:
                    return cycle

            elif neighbor in active:
                cycle = [neighbor]
                current = node

                while current != neighbor:
                    cycle.append(current)
                    current = parent[current]

                cycle.append(neighbor)
                cycle.reverse()
                return cycle

        active.remove(node)
        return None

    for node in graph:
        if node not in visited:
            parent[node] = None
            cycle = dfs(node)

            if cycle:
                return cycle

    return None


def analyze_repair(schedule):
    graph, edge_details = build_conflict_graph(schedule)
    cycle = find_cycle(graph)

    print("Conflict Graph:")
    for source in sorted(graph):
        for target in sorted(graph[source]):
            print(f"{source} -> {target}")

    if cycle is None:
        print("\nSchedule is conflict-serializable.")
        print("No repair needed.")
        return

    print("\nSchedule is NOT conflict-serializable.")
    print("Detected cycle:", " -> ".join(cycle))

    print("\nConflicts on this cycle:")
    for i in range(len(cycle) - 1):
        edge = (cycle[i], cycle[i + 1])

        for detail in edge_details[edge]:
            first, second, item, op1, op2 = detail
            print(
                f"Operations {first} and {second}: "
                f"{cycle[i]} {op1}({item}) before "
                f"{cycle[i + 1]} {op2}({item})"
            )

    print(
        "\nRepair idea: review one or more conflict edges "
        "on the cycle. Any change must preserve transaction "
        "semantics and required operation order."
    )


schedule = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T2", "W", "B"),
    ("T1", "R", "B"),
]

analyze_repair(schedule)
