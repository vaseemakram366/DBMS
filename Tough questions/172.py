# Blind Write Serializability Analyzer


from collections import defaultdict, deque
from itertools import permutations


def find_blind_writes(schedule):
    reads_by_transaction = defaultdict(set)

    for transaction, operation, item in schedule:
        if operation == "R":
            reads_by_transaction[transaction].add(item)

    blind_writes = []

    for position, (transaction, operation, item) in enumerate(
        schedule, start=1
    ):
        if operation == "W" and item not in reads_by_transaction[transaction]:
            blind_writes.append((position, transaction, item))

    return blind_writes


def build_conflict_graph(schedule):
    graph = defaultdict(set)
    transactions = {t for t, _, _ in schedule}

    for transaction in transactions:
        graph[transaction]

    for i, (t1, op1, item1) in enumerate(schedule):
        for t2, op2, item2 in schedule[i + 1:]:
            if t1 != t2 and item1 == item2:
                if op1 == "W" or op2 == "W":
                    graph[t1].add(t2)

    return graph, transactions


def has_cycle(graph, transactions):
    indegree = {t: 0 for t in transactions}

    for source in graph:
        for target in graph[source]:
            indegree[target] += 1

    queue = deque(t for t in transactions if indegree[t] == 0)
    processed = 0

    while queue:
        current = queue.popleft()
        processed += 1

        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return processed != len(transactions)


def view_signature(schedule):
    last_writer = {}
    read_sources = {}
    final_writers = {}

    for position, (transaction, operation, item) in enumerate(schedule):
        if operation == "R":
            source = last_writer.get(item, "INITIAL")
            read_sources[(transaction, item, position)] = source

        elif operation == "W":
            last_writer[item] = transaction
            final_writers[item] = transaction

    return read_sources, final_writers


def view_equivalent_to_serial(schedule, serial_order):
    # Build the serial schedule by preserving each transaction's
    # original internal operation order.
    serial_schedule = []

    for transaction in serial_order:
        serial_schedule.extend(
            operation
            for operation in schedule
            if operation[0] == transaction
        )

    # Match reads by transaction, item, and occurrence number.
    def normalized_signature(candidate):
        last_writer = {}
        read_counts = defaultdict(int)
        read_sources = {}
        final_writers = {}

        for transaction, operation, item in candidate:
            if operation == "R":
                key = (transaction, item, read_counts[(transaction, item)])
                read_counts[(transaction, item)] += 1
                read_sources[key] = last_writer.get(item, "INITIAL")

            elif operation == "W":
                last_writer[item] = transaction
                final_writers[item] = transaction

        return read_sources, final_writers

    return normalized_signature(schedule) == normalized_signature(serial_schedule)


def analyze_schedule(schedule):
    transactions = sorted({t for t, _, _ in schedule})
    blind_writes = find_blind_writes(schedule)
    graph, transactions_set = build_conflict_graph(schedule)
    cyclic = has_cycle(graph, transactions_set)

    view_serial_orders = []

    for order in permutations(transactions):
        if view_equivalent_to_serial(schedule, order):
            view_serial_orders.append(order)

    print("Transactions:", transactions)
    print("Blind writes:", blind_writes)
    print("Conflict graph:")

    for transaction in transactions:
        print(f"T{transaction} -> {sorted(graph[transaction])}")

    print("Conflict-serializable:", not cyclic)
    print("View-serializable:", bool(view_serial_orders))
    print("View-equivalent serial orders:", view_serial_orders)


if __name__ == "__main__":
    schedule = [
        (1, "W", "A"),
        (2, "W", "A"),
        (1, "W", "B"),
        (2, "W", "B"),
    ]

    analyze_schedule(schedule)
