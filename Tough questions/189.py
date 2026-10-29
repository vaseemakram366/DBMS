# Deadlock Detection Simulator


class DeadlockDetector:
    def __init__(self):
        self.graph = {}

    def add_transaction(self, transaction):
        if transaction not in self.graph:
            self.graph[transaction] = []

    def add_wait(self, waiting, blocking):
        self.add_transaction(waiting)
        self.add_transaction(blocking)

        if blocking not in self.graph[waiting]:
            self.graph[waiting].append(blocking)

        print(f"{waiting} waits for {blocking}")

    def detect_deadlock(self):
        visited = set()
        active = set()
        path = []

        def dfs(transaction):
            visited.add(transaction)
            active.add(transaction)
            path.append(transaction)

            for neighbor in self.graph[transaction]:
                if neighbor not in visited:
                    cycle = dfs(neighbor)
                    if cycle:
                        return cycle
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
                    print("Deadlock detected!")
                    print("Cycle:", " -> ".join(cycle))
                    return True

        print("No deadlock detected.")
        return False


detector = DeadlockDetector()

detector.add_wait("T1", "T2")
detector.add_wait("T2", "T3")
detector.add_wait("T3", "T1")

detector.detect_deadlock()
