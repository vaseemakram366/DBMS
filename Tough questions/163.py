# Incremental Conflict Graph Updater


from collections import defaultdict


class IncrementalConflictGraph:
    def __init__(self):
        self.graph = defaultdict(set)
        self.transactions = set()
        self.item_history = defaultdict(list)
        self.schedule = []

    def add_operation(self, transaction, operation, item):
        if operation not in ("R", "W"):
            raise ValueError("Operation must be R or W")

        self.transactions.add(transaction)
        self.graph[transaction]

        # Compare the new operation only with earlier operations
        # on the same data item.
        for old_transaction, old_operation in self.item_history[item]:
            if old_transaction == transaction:
                continue

            if old_operation == "W" or operation == "W":
                self.graph[old_transaction].add(transaction)

        self.item_history[item].append((transaction, operation))
        self.schedule.append((transaction, operation, item))

    def get_graph(self):
        return {
            transaction: sorted(self.graph[transaction])
            for transaction in sorted(self.transactions)
        }


def rebuild_graph(schedule):
    graph = defaultdict(set)
    transactions = set()

    for transaction, operation, item in schedule:
        transactions.add(transaction)
        graph[transaction]

    for i in range(len(schedule)):
        t1, op1, item1 = schedule[i]

        for j in range(i + 1, len(schedule)):
            t2, op2, item2 = schedule[j]

            if t1 != t2 and item1 == item2:
                if op1 == "W" or op2 == "W":
                    graph[t1].add(t2)

    return {
        transaction: sorted(graph[transaction])
        for transaction in sorted(transactions)
    }


if __name__ == "__main__":
    operations = [
        (1, "R", "A"),
        (2, "W", "A"),
        (3, "R", "B"),
        (3, "W", "A"),
        (1, "W", "B"),
        (2, "R", "B"),
    ]

    manager = IncrementalConflictGraph()

    for transaction, operation, item in operations:
        manager.add_operation(transaction, operation, item)

        print(
            f"Added T{transaction}: {operation}({item})"
        )
        print("Current graph:", manager.get_graph())
        print()

    rebuilt = rebuild_graph(manager.schedule)

    print("Incremental graph:", manager.get_graph())
    print("Rebuilt graph:    ", rebuilt)
    print("Validation:", manager.get_graph() == rebuilt)
    