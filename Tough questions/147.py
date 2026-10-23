# Conflict Serializability Checker


from collections import defaultdict


class ConflictSerializabilityChecker:
    def __init__(self, schedule):
        # Each operation: (transaction, operation, data_item)
        self.schedule = schedule
        self.graph = defaultdict(set)
        self.transactions = set()

    def build_graph(self):
        n = len(self.schedule)

        for tx, operation, item in self.schedule:
            self.transactions.add(tx)
            self.graph[tx]

        for i in range(n):
            tx1, op1, item1 = self.schedule[i]

            for j in range(i + 1, n):
                tx2, op2, item2 = self.schedule[j]

                # Same transaction or different data items:
                # no inter-transaction conflict
                if tx1 == tx2 or item1 != item2:
                    continue

                # At least one operation must be a write
                if op1 == "W" or op2 == "W":
                    self.graph[tx1].add(tx2)

    def find_serial_order(self):
        indegree = {tx: 0 for tx in self.transactions}

        for tx in self.graph:
            for neighbor in self.graph[tx]:
                indegree[neighbor] += 1

        queue = [
            tx for tx in self.transactions
            if indegree[tx] == 0
        ]

        order = []

        while queue:
            tx = queue.pop(0)
            order.append(tx)

            for neighbor in self.graph[tx]:
                indegree[neighbor] -= 1

                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) == len(self.transactions):
            return order

        return None

    def check(self):
        self.build_graph()

        print("Precedence graph:")
        for tx in sorted(self.transactions):
            print(f"{tx} -> {sorted(self.graph[tx])}")

        order = self.find_serial_order()

        if order is None:
            print("\nSchedule is NOT conflict-serializable")
            print("Reason: precedence graph contains a cycle")
            return False

        print("\nSchedule IS conflict-serializable")
        print("Equivalent serial order:", " -> ".join(order))
        return True


# Example 1: Serializable schedule
schedule1 = [
    ("T1", "R", "A"),
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T2", "W", "A")
]

print("=== Schedule 1 ===")
checker1 = ConflictSerializabilityChecker(schedule1)
checker1.check()

# Example 2: Non-serializable schedule
schedule2 = [
    ("T1", "W", "A"),
    ("T2", "W", "A"),
    ("T2", "W", "B"),
    ("T1", "W", "B")
]

print("\n=== Schedule 2 ===")
checker2 = ConflictSerializabilityChecker(schedule2)
checker2.check()
