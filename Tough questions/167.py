# Conflict Graph Repair Cost Analyzer


from collections import defaultdict, deque
from itertools import combinations


class ConflictGraphRepairCostAnalyzer:
    def __init__(self, transactions, weighted_edges):
        self.transactions = set(transactions)
        self.edge_costs = {}

        for source, target, cost in weighted_edges:
            if cost < 0:
                raise ValueError("Repair costs must be non-negative")

            self.transactions.update([source, target])
            self.edge_costs[(source, target)] = cost

    def is_acyclic(self, edges):
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

        return processed == len(self.transactions)

    def find_minimum_cost_repair(self):
        edges = sorted(self.edge_costs)
        best_cost = float("inf")
        best_removed = []
        best_remaining = []

        for count in range(len(edges) + 1):
            for removed_tuple in combinations(edges, count):
                removed = set(removed_tuple)
                remaining = set(edges) - removed

                cost = sum(self.edge_costs[e] for e in removed)

                if cost > best_cost:
                    continue

                if self.is_acyclic(remaining):
                    if cost < best_cost:
                        best_cost = cost
                        best_removed = list(removed_tuple)
                        best_remaining = sorted(remaining)

        return best_cost, best_removed, best_remaining

    def analyze(self):
        edges = set(self.edge_costs)

        print("Original weighted edges:")
        for edge in sorted(edges):
            print(f"{edge[0]} -> {edge[1]} | Cost: {self.edge_costs[edge]}")

        print("\nOriginal graph acyclic:", self.is_acyclic(edges))

        cost, removed, remaining = self.find_minimum_cost_repair()

        print("\nMinimum repair cost:", cost)
        print("Edges to remove:", removed)
        print("Remaining edges:", remaining)
        print("Final graph acyclic:", self.is_acyclic(set(remaining)))


if __name__ == "__main__":
    transactions = [1, 2, 3]

    weighted_edges = [
        (1, 2, 5),
        (2, 3, 2),
        (3, 1, 8),
    ]

    analyzer = ConflictGraphRepairCostAnalyzer(
        transactions, weighted_edges
    )
    analyzer.analyze()
