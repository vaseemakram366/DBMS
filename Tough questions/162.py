# Optimized Conflict Graph Builder


from collections import defaultdict
from time import perf_counter
import random


def naive_conflict_graph(schedule):
    graph = defaultdict(set)
    transactions = set()

    for transaction, _, _ in schedule:
        transactions.add(transaction)
        graph[transaction]

    for i in range(len(schedule)):
        t1, op1, item1 = schedule[i]

        for j in range(i + 1, len(schedule)):
            t2, op2, item2 = schedule[j]

            if t1 == t2 or item1 != item2:
                continue

            if op1 == "W" or op2 == "W":
                graph[t1].add(t2)

    return graph, transactions


def optimized_conflict_graph(schedule):
    graph = defaultdict(set)
    transactions = set()

    # Per data item: track the latest writer and active readers.
    last_writer = {}
    readers = defaultdict(set)

    for transaction, operation, item in schedule:
        transactions.add(transaction)
        graph[transaction]

        if operation == "R":
            # A previous write conflicts with this read.
            writer = last_writer.get(item)

            if writer is not None and writer != transaction:
                graph[writer].add(transaction)

            readers[item].add(transaction)

        elif operation == "W":
            # Previous write conflicts with this write.
            writer = last_writer.get(item)

            if writer is not None and writer != transaction:
                graph[writer].add(transaction)

            # Every previous read conflicts with this write.
            for reader in readers[item]:
                if reader != transaction:
                    graph[reader].add(transaction)

            # This write replaces the previous writer.
            readers[item].clear()
            last_writer[item] = transaction

        else:
            raise ValueError(f"Invalid operation: {operation}")

    return graph, transactions


def normalize_graph(graph, transactions):
    return {
        transaction: sorted(graph[transaction])
        for transaction in sorted(transactions)
    }


def generate_schedule(transaction_count, operations_per_transaction):
    schedule = []

    for transaction in range(1, transaction_count + 1):
        for _ in range(operations_per_transaction):
            operation = random.choice(["R", "W"])
            item = random.choice(["A", "B", "C", "D", "E"])
            schedule.append((transaction, operation, item))

    random.shuffle(schedule)
    return schedule


if __name__ == "__main__":
    schedule = [
        (1, "R", "A"),
        (2, "W", "A"),
        (3, "R", "A"),
        (1, "W", "B"),
        (3, "W", "A"),
        (2, "R", "B"),
    ]

    print("Transaction Schedule:")
    for transaction, operation, item in schedule:
        print(f"T{transaction}: {operation}({item})")

    naive_graph, naive_transactions = naive_conflict_graph(schedule)
    fast_graph, fast_transactions = optimized_conflict_graph(schedule)

    print("\nNaive Conflict Graph:")
    print(normalize_graph(naive_graph, naive_transactions))

    print("\nOptimized Conflict Graph:")
    print(normalize_graph(fast_graph, fast_transactions))

    assert normalize_graph(naive_graph, naive_transactions) == \
           normalize_graph(fast_graph, fast_transactions)

    print("\nValidation: Both graphs are identical.")

    # Benchmark both methods on the same generated schedule.
    random.seed(42)
    large_schedule = generate_schedule(30, 20)

    start = perf_counter()
    naive_conflict_graph(large_schedule)
    naive_time = perf_counter() - start

    start = perf_counter()
    optimized_conflict_graph(large_schedule)
    optimized_time = perf_counter() - start

    print("\nBenchmark: 600 operations")
    print(f"Naive builder:     {naive_time:.6f} seconds")
    print(f"Optimized builder: {optimized_time:.6f} seconds")

    if optimized_time > 0:
        print(f"Speedup: {naive_time / optimized_time:.2f}x")
