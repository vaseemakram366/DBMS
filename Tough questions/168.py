# Transaction Serialization Order Optimizer


from collections import defaultdict
import heapq


class SerializationOrderOptimizer:
    def __init__(self, transactions, edges):
        self.transactions = set(transactions)
        self.edges = set(edges)

        for source, target in self.edges:
            self.transactions.update([source, target])

        self.graph = defaultdict(set)
        self.indegree = {
            transaction: 0 for transaction in self.transactions
        }

        for source, target in self.edges:
            if target not in self.graph[source]:
                self.graph[source].add(target)
                self.indegree[target] += 1

    def find_one_order(self):
        indegree = self.indegree.copy()
        heap = [
            transaction
            for transaction in self.transactions
            if indegree[transaction] == 0
        ]
        heapq.heapify(heap)

        order = []

        while heap:
            current = heapq.heappop(heap)
            order.append(current)

            for neighbor in sorted(self.graph[current]):
                indegree[neighbor] -= 1

                if indegree[neighbor] == 0:
                    heapq.heappush(heap, neighbor)

        if len(order) != len(self.transactions):
            return None

        return order

    def find_all_orders(self):
        indegree = self.indegree.copy()
        order = []
        all_orders = []

        def backtrack():
            if len(order) == len(self.transactions):
                all_orders.append(order.copy())
                return

            available = sorted(
                transaction
                for transaction in self.transactions
                if indegree[transaction] == 0
                and transaction not in order
            )

            for current in available:
                order.append(current)

                for neighbor in self.graph[current]:
                    indegree[neighbor] -= 1

                backtrack()

                for neighbor in self.graph[current]:
                    indegree[neighbor] += 1

                order.pop()

        backtrack()
        return all_orders

    def analyze(self):
        print("Transactions:", sorted(self.transactions))
        print("Conflict edges:", sorted(self.edges))

        one_order = self.find_one_order()

        if one_order is None:
            print("\nCycle detected: no valid serial order exists.")
            return

        print("\nOne valid serial order:",
              " -> ".join(f"T{t}" for t in one_order))

        all_orders = self.find_all_orders()

        print("\nAll valid serial orders:")
        for index, order in enumerate(all_orders, start=1):
            print(f"{index}. " + " -> ".join(f"T{t}" for t in order))

        print("\nTotal valid serial orders:", len(all_orders))


if __name__ == "__main__":
    transactions = [1, 2, 3, 4]

    edges = [
        (1, 2),
        (1, 3),
        (2, 4),
        (3, 4),
    ]

    optimizer = SerializationOrderOptimizer(transactions, edges)
    optimizer.analyze()
