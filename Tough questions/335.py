# Database Serializability Checker


from collections import defaultdict

class SerializabilityChecker:
    def __init__(self, schedule):
        self.schedule = schedule
        self.graph = defaultdict(set)

    def build_graph(self):
        n = len(self.schedule)

        for i in range(n):
            tx1, op1, item1 = self.schedule[i]

            for j in range(i + 1, n):
                tx2, op2, item2 = self.schedule[j]

                if tx1 == tx2 or item1 != item2:
                    continue

                if op1 == "W" or op2 == "W":
                    self.graph[tx1].add(tx2)

    def has_cycle(self):
        visited = set()
        path = set()

        def dfs(node):
            visited.add(node)
            path.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in path:
                    return True

            path.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return True

        return False

    def check(self):
        self.build_graph()

        print("Precedence Graph:")

        for tx, neighbors in self.graph.items():
            print(tx, "->", list(neighbors))

        if self.has_cycle():
            print("Schedule is NOT Conflict Serializable")
        else:
            print("Schedule is Conflict Serializable")


schedule = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T2", "W", "B"),
    ("T1", "R", "B")
]

obj = SerializabilityChecker(schedule)
obj.check()
