# Transaction Recovery Order Planner


from collections import defaultdict, deque


def recovery_order(schedule):
    last_writer = {}
    transactions = set()
    dependencies = set()

    for op, tid, item in schedule:
        transactions.add(tid)

        if op == "W":
            last_writer[item] = tid

        elif op == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != tid:
                dependencies.add((writer, tid))

    graph = defaultdict(set)
    indegree = {tid: 0 for tid in transactions}

    for writer, reader in dependencies:
        if reader not in graph[writer]:
            graph[writer].add(reader)
            indegree[reader] += 1

    queue = deque(
        tid for tid in sorted(transactions)
        if indegree[tid] == 0
    )

    order = []

    while queue:
        tid = queue.popleft()
        order.append(tid)

        for neighbor in sorted(graph[tid]):
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if len(order) != len(transactions):
        return None, dependencies

    return order, dependencies


def main():
    schedule = [
        ("W", 1, "A"),
        ("R", 2, "A"),
        ("W", 2, "B"),
        ("R", 3, "B"),
        ("C", 1, None),
        ("C", 2, None),
        ("C", 3, None),
    ]

    order, dependencies = recovery_order(schedule)

    print("Read-from dependencies:")
    for writer, reader in sorted(dependencies):
        print(f"T{writer} -> T{reader}")

    if order is None:
        print("\nNo valid recovery order: dependency cycle found.")
    else:
        print("\nValid commit order:")
        print(" -> ".join(f"T{tid}" for tid in order))


if __name__ == "__main__":
    main()
