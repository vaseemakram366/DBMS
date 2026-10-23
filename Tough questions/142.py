# Wait-For Graph Deadlock Detector


class WaitForGraph:
    def __init__(self):
        self.graph = {}

    def add_transaction(self, tx):
        self.graph.setdefault(tx, [])

    def add_wait(self, waiting_tx, holding_tx):
        self.add_transaction(waiting_tx)
        self.add_transaction(holding_tx)

        if holding_tx not in self.graph[waiting_tx]:
            self.graph[waiting_tx].append(holding_tx)

        print(f"Added dependency: {waiting_tx} -> {holding_tx}")

    def remove_wait(self, waiting_tx, holding_tx):
        if waiting_tx in self.graph:
            if holding_tx in self.graph[waiting_tx]:
                self.graph[waiting_tx].remove(holding_tx)
                print(f"Removed dependency: {waiting_tx} -> {holding_tx}")

    def find_deadlock(self):
        visited = set()
        active = set()
        path = []

        def dfs(tx):
            visited.add(tx)
            active.add(tx)
            path.append(tx)

            for neighbor in self.graph.get(tx, []):
                if neighbor not in visited:
                    cycle = dfs(neighbor)
                    if cycle:
                        return cycle

                elif neighbor in active:
                    start = path.index(neighbor)
                    return path[start:] + [neighbor]

            path.pop()
            active.remove(tx)
            return None

        for tx in self.graph:
            if tx not in visited:
                cycle = dfs(tx)
                if cycle:
                    print("Deadlock detected!")
                    print("Cycle:", " -> ".join(cycle))
                    return cycle

        print("No deadlock detected.")
        return None

    def show_graph(self):
        print("\nWait-For Graph:")
        for tx, dependencies in self.graph.items():
            print(f"{tx} waits for: {dependencies}")


# Demonstration
wfg = WaitForGraph()

wfg.add_wait("T1", "T2")
wfg.add_wait("T2", "T3")
wfg.add_wait("T3", "T1")
wfg.add_wait("T4", "T2")

wfg.show_graph()
wfg.find_deadlock()
