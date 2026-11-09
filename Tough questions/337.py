# Conflict Serializability Using Topological Sort


from collections import defaultdict, deque

class ConflictSerializability:
    def __init__(self, schedule):
        self.schedule = schedule
        self.graph = defaultdict(set)

    def build_graph(self):
        transactions = set()

        for tx, op, item in self.schedule:
            transactions.add(tx)

        for tx in transactions:
            self.graph[tx]

        n = len(self.schedule)

        for i in range(n):
            tx1, op1, item1 = self.schedule[i]

            for j in range(i + 1, n):
                tx2, op2, item2 = self.schedule[j]

                if tx1 != tx2 and item1 == item2:
                    if op1 == "W" or op2 == "W":
                        self.graph[tx1].add(tx2)

    def topological_sort(self):
        indegree = {tx: 0 for tx in self.graph}

        for node in self.graph:
            for neighbor in self.graph[node]:
                indegree[neighbor] += 1

        queue = deque(
            tx for tx in indegree if indegree[tx] == 0
        )

        order = []

        while queue:
            node = queue.popleft()
            order.append(node)

            for neighbor in self.graph[node]:
                indegree[neighbor] -= 1

                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) == len(indegree):
            print("Conflict Serializable")
            print("Serial Order:", order)
        else:
            print("Not Conflict Serializable: Cycle Found")


schedule = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T2", "W", "B"),
    ("T3", "R", "B")
]

obj = ConflictSerializability(schedule)
obj.build_graph()
obj.topological_sort()
