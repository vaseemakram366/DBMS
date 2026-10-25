# Transaction Schedule Generator and Validator


import random
from collections import defaultdict, deque


def generate_schedule(num_transactions=3, operations_per_tx=3):
    schedule = []
    items = ["A", "B", "C"]

    for i in range(1, num_transactions + 1):
        tx = f"T{i}"
        operations = []

        for _ in range(operations_per_tx):
            op = random.choice(["R", "W"])
            item = random.choice(items)
            operations.append((tx, op, item))

        operations.append((tx, "C", ""))
        schedule.extend(operations)

    random.shuffle(schedule)

    # Keep each transaction's operations in their original order.
    # Rebuild a valid interleaving from per-transaction queues.
    per_tx = defaultdict(deque)
    for tx, op, item in schedule:
        per_tx[tx].append((tx, op, item))

    result = []
    while per_tx:
        tx = random.choice(list(per_tx))
        result.append(per_tx[tx].popleft())
        if not per_tx[tx]:
            del per_tx[tx]

    return result


def validate_schedule(schedule):
    graph = defaultdict(set)
    transactions = set()
    last_writer = {}
    readers = defaultdict(set)
    committed = set()
    active_writers = {}
    dependencies = []

    recoverable = True
    cascadeless = True
    strict = True

    for tx, op, item in schedule:
        transactions.add(tx)

        if op == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != tx:
                graph[writer].add(tx)
                dependencies.append((writer, tx))

                if writer not in committed:
                    cascadeless = False

            if item in active_writers and active_writers[item] != tx:
                strict = False

            readers[item].add(tx)

        elif op == "W":
            writer = last_writer.get(item)

            if writer is not None and writer != tx:
                graph[writer].add(tx)

            if item in active_writers and active_writers[item] != tx:
                strict = False

            for reader in readers[item]:
                if reader != tx:
                    graph[reader].add(tx)

            active_writers[item] = tx
            last_writer[item] = tx
            readers[item].clear()

        elif op == "C":
            committed.add(tx)

            for writer, reader in dependencies:
                if reader == tx and writer not in committed:
                    recoverable = False

            for data_item in list(active_writers):
                if active_writers[data_item] == tx:
                    del active_writers[data_item]

        elif op == "A":
            for data_item in list(active_writers):
                if active_writers[data_item] == tx:
                    del active_writers[data_item]

    nodes = transactions | set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors)

    indegree = {tx: 0 for tx in nodes}

    for tx in graph:
        for neighbor in graph[tx]:
            indegree[neighbor] += 1

    queue = deque(tx for tx in nodes if indegree[tx] == 0)
    visited = 0

    while queue:
        tx = queue.popleft()
        visited += 1

        for neighbor in graph[tx]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return {
        "Conflict-serializable": visited == len(nodes),
        "Recoverable": recoverable,
        "Cascadeless": cascadeless,
        "Strict": strict,
    }


random.seed(10)

schedule = generate_schedule(
    num_transactions=3,
    operations_per_tx=3
)

print("Generated Schedule:")
for tx, op, item in schedule:
    if op in ("R", "W"):
        print(f"{tx}: {op}({item})")
    else:
        print(f"{tx}: COMMIT")

print("\nValidation Results:")
for property_name, result in validate_schedule(schedule).items():
    print(f"{property_name}: {result}")
