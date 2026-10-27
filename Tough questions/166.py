# Minimum Feedback Arc Set Heuristic


from collections import defaultdict, deque


class FeedbackArcHeuristic:
    def __init__(self, transactions, edges):
        self.transactions = set(transactions)
        self.edges = set(edges)

        for u, v in self.edges:
            self.transactions.update([u, v])

    def build_graph(self, edges):
        graph = defaultdict(list)

        for t in self.transactions:
            graph[t]

        for u, v in edges:
            graph[u].append(v)

        return graph

    def find_cycle(self, edges):
        graph = self.build_graph(edges)
        color = {t: 0 for t in self.transactions}
        parent = {}

        def dfs(node):
            color[node] = 1

            for neighbor in graph[node]:
                if color[neighbor] == 0:
                    parent[neighbor] = node
                    cycle = dfs(neighbor)

                    if cycle:
                        return cycle

                elif color[neighbor] == 1:
                    # Back edge: reconstruct one directed cycle.
                    cycle = [(node, neighbor)]
                    current = node

                    while current != neighbor:
                        previous = parent[current]
                        cycle.append((previous, current))
                        current = previous

                    return cycle

            color[node] = 2
            return None

        for transaction in sorted(self.transactions):
            if color[transaction] == 0:
                cycle = dfs(transaction)

                if cycle:
                    return cycle

        return None

    def is_acyclic(self, edges):
        graph = self.build_graph(edges)
        indegree = {t: 0 for t in self.transactions}

        for u, v in edges:
            indegree[v] += 1

        queue = deque(
            t for t in self.transactions if indegree[t] == 0
        )

        visited = 0

        while queue:
            node = queue.popleft()
            visited += 1

            for neighbor in graph[node]:
                indegree[neighbor] -= 1

                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return visited == len(self.transactions)

    def repair(self):
        remaining = set(self.edges)
        removed = []

        while True:
            cycle = self.find_cycle(remaining)

            if cycle is None:
                break

            # Deterministic heuristic: remove the
            # lexicographically largest edge in this cycle.
            edge_to_remove = max(cycle)
            remaining.remove(edge_to_remove)
            removed.append(edge_to_remove)

            print("Cycle found:", cycle)
            print("Removed edge:", edge_to_remove)

        return removed, remaining


if __name__ == "__main__":
    transactions = [1, 2, 3, 4]

    edges = [
        (1, 2),
        (2, 3),
        (3, 1),
        (3, 4),
        (4, 2),
    ]

    optimizer = FeedbackArcHeuristic(transactions, edges)

    print("Original edges:", sorted(optimizer.edges))
    print("Original graph acyclic:",
          optimizer.is_acyclic(optimizer.edges))
    print()

    removed, remaining = optimizer.repair()

    print("\nRemoved edges:", sorted(removed))
    print("Remaining edges:", sorted(remaining))
    print("Final graph acyclic:", optimizer.is_acyclic(remaining))
