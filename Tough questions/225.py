# Deadlock Prevention Simulator


class DeadlockPrevention:
    def __init__(self):
        self.graph = {}

    def add_transaction(self, transaction):
        self.graph.setdefault(transaction, [])

    def has_cycle(self):
        visited = set()
        active = set()

        def dfs(node):
            visited.add(node)
            active.add(node)

            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in active:
                    return True

            active.remove(node)
            return False

        for node in self.graph:
            if node not in visited:
                if dfs(node):
                    return True

        return False

    def request_wait(self, waiting, holding):
        self.add_transaction(waiting)
        self.add_transaction(holding)

        self.graph[waiting].append(holding)

        if self.has_cycle():
            self.graph[waiting].pop()
            print(f"Request rejected: {waiting} -> {holding}")
            return False

        print(f"Request accepted: {waiting} -> {holding}")
        return True


manager = DeadlockPrevention()

manager.request_wait("T1", "T2")
manager.request_wait("T2", "T3")
manager.request_wait("T3", "T1")
