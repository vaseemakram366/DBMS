# All Valid Serial Orders Generator


def all_serial_orders(graph):
    nodes = set(graph)

    for neighbors in graph.values():
        nodes.update(neighbors)

    indegree = {tx: 0 for tx in nodes}

    for source in graph:
        for target in graph[source]:
            indegree[target] += 1

    results = []

    def backtrack(order, current_indegree, remaining):
        if not remaining:
            results.append(order.copy())
            return

        available = sorted(
            tx for tx in remaining
            if current_indegree[tx] == 0
        )

        for tx in available:
            next_indegree = current_indegree.copy()
            next_remaining = remaining - {tx}

            for neighbor in graph.get(tx, set()):
                next_indegree[neighbor] -= 1

            order.append(tx)
            backtrack(order, next_indegree, next_remaining)
            order.pop()

    backtrack([], indegree, nodes)

    return results


graph = {
    "T1": {"T3"},
    "T2": {"T3"},
    "T3": set()
}

orders = all_serial_orders(graph)

if orders:
    print("All Valid Serial Orders:")
    for order in orders:
        print(" -> ".join(order))
    print("Total orders:", len(orders))
else:
    print("No valid serial order: dependency graph contains a cycle.")
