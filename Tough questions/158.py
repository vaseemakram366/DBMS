# Transaction Schedule Topological Sorter


from collections import defaultdict, deque


def topological_sort(graph):
    nodes = set(graph)

    for neighbors in graph.values():
        nodes.update(neighbors)

    indegree = {node: 0 for node in nodes}

    for source in graph:
        for target in graph[source]:
            indegree[target] += 1

    queue = deque(
        sorted(node for node in nodes if indegree[node] == 0)
    )

    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for neighbor in sorted(graph.get(node, set())):
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(nodes):
        print("Cycle detected!")
        print("No conflict-equivalent serial order exists.")
        return None

    return order


def show_serial_order(graph):
    order = topological_sort(graph)

    if order is not None:
        print("Valid serial order:")
        print(" -> ".join(order))


graph1 = defaultdict(set)
graph1["T1"].update(["T2", "T3"])
graph1["T2"].add("T3")
graph1["T3"]

print("Example 1:")
show_serial_order(graph1)

graph2 = defaultdict(set)
graph2["T1"].add("T2")
graph2["T2"].add("T1")

print("\nExample 2:")
show_serial_order(graph2)
