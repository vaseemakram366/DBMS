# Database Lock Wait Graph Analyzer


class LockWaitGraphAnalyzer:

    def __init__(self):
        self.graph = {}

    def add_transaction(self, transaction):
        if transaction not in self.graph:
            self.graph[transaction] = []

    def add_wait(self, waiting_tx, blocking_tx):
        self.add_transaction(waiting_tx)
        self.add_transaction(blocking_tx)

        if blocking_tx not in self.graph[waiting_tx]:
            self.graph[waiting_tx].append(blocking_tx)

    def find_cycle(self):
        visited = set()
        active = set()
        path = []

        def dfs(transaction):
            visited.add(transaction)
            active.add(transaction)
            path.append(transaction)

            for neighbor in self.graph[transaction]:
                if neighbor not in visited:
                    result = dfs(neighbor)
                    if result:
                        return result

                elif neighbor in active:
                    start = path.index(neighbor)
                    return path[start:] + [neighbor]

            path.pop()
            active.remove(transaction)
            return None

        for transaction in self.graph:
            if transaction not in visited:
                cycle = dfs(transaction)
                if cycle:
                    return cycle

        return None

    def display_graph(self):
        print("WAIT-FOR GRAPH")

        for transaction, blockers in self.graph.items():
            print(f"{transaction} -> {blockers}")

        cycle = self.find_cycle()

        if cycle:
            print("\nDEADLOCK DETECTED!")
            print("Cycle:", " -> ".join(cycle))
        else:
            print("\nNo deadlock detected.")


analyzer = LockWaitGraphAnalyzer()

analyzer.add_wait("T1", "T2")
analyzer.add_wait("T2", "T3")
analyzer.add_wait("T3", "T1")

analyzer.display_graph()
