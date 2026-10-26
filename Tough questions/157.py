# Transaction Schedule Dependency Visualizer


from collections import defaultdict, deque


def visualize_dependencies(schedule):
    graph = defaultdict(set)
    transactions = set()
    last_writer = {}
    readers = defaultdict(set)

    for tx, op, item in schedule:
        transactions.add(tx)

        if op == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != tx:
                graph[writer].add(tx)

            readers[item].add(tx)

        elif op == "W":
            writer = last_writer.get(item)

            if writer is not None and writer != tx:
                graph[writer].add(tx)

            for reader in readers[item]:
                if reader != tx:
                    graph[reader].add(tx)

            last_writer[item] = tx
            readers[item].clear()

    for tx in transactions:
        graph[tx]  # Include transactions with no dependencies.

    print("Dependency Graph:")
    has_edge = False

    for source in sorted(graph):
        for target in sorted(graph[source]):
            print(f"{source} -> {target}")
            has_edge = True

    if not has_edge:
        print("No dependencies")

    # Kahn's algorithm: detect cycles.
    indegree = {tx: 0 for tx in graph}

    for source in graph:
        for target in graph[source]:
            indegree[target] += 1

    queue = deque(
        tx for tx in graph if indegree[tx] == 0
    )
    visited = 0

    while queue:
        tx = queue.popleft()
        visited += 1

        for target in graph[tx]:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)

    print(
        "Conflict-serializable:",
        visited == len(graph)
    )


schedule = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T2", "W", "B"),
    ("T1", "R", "B"),
]

visualize_dependencies(schedule)
