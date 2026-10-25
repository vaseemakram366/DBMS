# Transaction Schedule Classifier


from collections import defaultdict


def classify_schedule(schedule):
    graph = defaultdict(set)
    transactions = set()
    last_writer = {}
    readers = defaultdict(set)
    dependencies = []
    committed = set()
    active_writers = {}
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

    # Detect cycles in the precedence graph.
    nodes = transactions | set(graph.keys())
    for neighbors in graph.values():
        nodes.update(neighbors)

    indegree = {tx: 0 for tx in nodes}

    for tx in graph:
        for neighbor in graph[tx]:
            indegree[neighbor] += 1

    queue = [tx for tx in nodes if indegree[tx] == 0]
    visited = 0

    while queue:
        tx = queue.pop()
        visited += 1

        for neighbor in graph[tx]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    conflict_serializable = visited == len(nodes)

    print("Schedule Classification")
    print("-----------------------")
    print("Conflict-serializable:", conflict_serializable)
    print("Recoverable:", recoverable)
    print("Cascadeless:", cascadeless)
    print("Strict:", strict)


schedule = [
    ("T1", "W", "A"),
    ("T1", "C", ""),
    ("T2", "R", "A"),
    ("T2", "W", "B"),
    ("T2", "C", "")
]

classify_schedule(schedule)
