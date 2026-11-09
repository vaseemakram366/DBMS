# Transaction Dependency Graph


from collections import defaultdict

class TransactionDependencyGraph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_dependency(self, tx1, tx2):
        self.graph[tx1].append(tx2)
        self.graph[tx2]

    def display(self):
        print("Transaction Dependencies:")

        for tx in self.graph:
            print(tx, "->", self.graph[tx])

    def detect_cycle(self):
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


obj = TransactionDependencyGraph()

obj.add_dependency("T1", "T2")
obj.add_dependency("T2", "T3")
obj.add_dependency("T1", "T3")

obj.display()

print("Cycle Found:", obj.detect_cycle())
