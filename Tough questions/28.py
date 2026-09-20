# Conflict Serializability Checker

from collections import defaultdict, deque


class SerializabilityChecker:
    def __init__(self, schedule):
        self.schedule = schedule
        self.graph = defaultdict(set)
        self.transactions = set()

    def build_graph(self):
        for transaction, operation, item in self.schedule:
            self.transactions.add(transaction)

        for i in range(len(self.schedule)):
            t1, op1, item1 = self.schedule[i]

            for j in range(i + 1, len(self.schedule)):
                t2, op2, item2 = self.schedule[j]

                if t1 == t2:
                    continue

                if item1 != item2:
                    continue

                if op1 == "R" and op2 == "R":
                    continue

                self.graph[t1].add(t2)

    def has_cycle(self):
        indegree = {t: 0 for t in self.transactions}

        for u in self.graph:
            for v in self.graph[u]:
                indegree[v] += 1

        queue = deque(
            t for t in self.transactions
            if indegree[t] == 0
        )

        processed = 0

        while queue:
            u = queue.popleft()
            processed += 1

            for v in self.graph[u]:
                indegree[v] -= 1

                if indegree[v] == 0:
                    queue.append(v)

        return processed != len(self.transactions)

    def get_serial_order(self):
        indegree = {t: 0 for t in self.transactions}

        for u in self.graph:
            for v in self.graph[u]:
                indegree[v] += 1

        queue = deque(
            t for t in self.transactions
            if indegree[t] == 0
        )

        order = []

        while queue:
            u = queue.popleft()
            order.append(u)

            for v in self.graph[u]:
                indegree[v] -= 1

                if indegree[v] == 0:
                    queue.append(v)

        return order

    def check(self):
        self.build_graph()

        if self.has_cycle():
            return False, []

        return True, self.get_serial_order()


schedule = [
    ("T1", "R", "A"),
    ("T2", "R", "B"),
    ("T1", "W", "B"),
    ("T2", "W", "A")
]

checker = SerializabilityChecker(schedule)

serializable, order = checker.check()

print("Conflict Serializable:", serializable)

if serializable:
    print("Equivalent Serial Order:", order)
else:
    print("Cycle detected in precedence graph")