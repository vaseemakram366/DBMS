# Transaction Schedule Serializability Benchmark


import random
import time
from collections import defaultdict, deque


def generate_schedule(num_transactions, operations_per_tx, seed=42):
    rng = random.Random(seed)
    queues = []

    for i in range(num_transactions):
        tx = f"T{i + 1}"
        operations = [
            (tx, rng.choice(["R", "W"]), rng.choice(["A", "B", "C", "D"]))
            for _ in range(operations_per_tx)
        ]
        queues.append(operations)

    schedule = []

    while any(queues):
        available = [i for i, q in enumerate(queues) if q]
        index = rng.choice(available)
        schedule.append(queues[index].pop(0))

    return schedule


def build_graph(schedule):
    graph = defaultdict(set)
    transactions = {tx for tx, _, _ in schedule}

    for tx in transactions:
        graph[tx]

    for i, (tx1, op1, item1) in enumerate(schedule):
        for tx2, op2, item2 in schedule[i + 1:]:
            if tx1 != tx2 and item1 == item2:
                if op1 == "W" or op2 == "W":
                    graph[tx1].add(tx2)

    return graph


def is_acyclic(graph):
    nodes = set(graph)

    for neighbors in graph.values():
        nodes.update(neighbors)

    indegree = {node: 0 for node in nodes}

    for source in graph:
        for target in graph[source]:
            indegree[target] += 1

    queue = deque(
        node for node in nodes if indegree[node] == 0
    )
    visited = 0

    while queue:
        node = queue.popleft()
        visited += 1

        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return visited == len(nodes)


def benchmark(num_transactions, operations_per_tx, seed=42):
    schedule = generate_schedule(
        num_transactions, operations_per_tx, seed
    )

    start = time.perf_counter()
    graph = build_graph(schedule)
    graph_time = time.perf_counter() - start

    start = time.perf_counter()
    result = is_acyclic(graph)
    cycle_time = time.perf_counter() - start

    return len(schedule), graph_time, cycle_time, result


if __name__ == "__main__":
    test_sizes = [5, 10, 20, 40]

    print(
        f"{'Transactions':<15}{'Operations':<15}"
        f"{'Graph (ms)':<15}{'Cycle (ms)':<15}{'Serializable'}"
    )

    for count in test_sizes:
        operations, graph_ms, cycle_ms, result = benchmark(
            count, operations_per_tx=10, seed=42
        )

        print(
            f"{count:<15}{operations:<15}"
            f"{graph_ms * 1000:<15.3f}"
            f"{cycle_ms * 1000:<15.3f}{result}"
        )
