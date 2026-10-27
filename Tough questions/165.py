# Transaction Schedule Repairer


from collections import defaultdict, deque
from itertools import combinations


class TransactionScheduleRepairer:
    def __init__(self, transactions, edges):
        self.transactions = set(transactions)
        self.edges = set(edges)

        for source, target in self.edges:
            self.transactions.add(source)
            self.transactions.add(target)

    def has_cycle(self, edges):
        graph = defaultdict(list)
        indegree = {t: 0 for t in self.transactions}

        for source, target in edges:
            graph[source].append(target)
            indegree[target] += 1

        queue = deque(
            t for t in self.transactions if indegree[t] == 0
        )

        processed = 0

        while queue:
            current = queue.popleft()
            processed += 1

            for neighbor in graph[current]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return processed != len(self.transactions)

    def find_repairs(self):
        # Find the smallest number of edges whose removal
        # makes the graph acyclic.
        ordered_edges = sorted(self.edges)

        for remove_count in range(len(ordered_edges) + 1):
            repairs = []

            for removed in combinations(ordered_edges, remove_count):
                removed_set = set(removed)
                remaining = self.edges - removed_set

                if not self.has_cycle(remaining):
                    repairs.append({
                        "removed_edges": list(removed),
                        "remaining_edges": sorted(remaining)
                    })

            if repairs:
                return repairs

        return []

    def display(self):
        print("Transactions:", sorted(self.transactions))
        print("Conflict edges:", sorted(self.edges))
        print("Has cycle:", self.has_cycle(self.edges))

        repairs = self.find_repairs()

        print("\nMinimum edge-removal repair options:")
        for index, repair in enumerate(repairs, start=1):
            print(f"\nOption {index}:")
            print("Remove:", repair["removed_edges"])
            print("Remaining:", repair["remaining_edges"])
            print("Acyclic:", not self.has_cycle(
                set(repair["remaining_edges"])
            ))


if __name__ == "__main__":
    transactions = [1, 2, 3]
    edges = [
        (1, 2),
        (2, 3),
        (3, 1),
    ]

    repairer = TransactionScheduleRepairer(
        transactions, edges
    )
    repairer.display()
