# Deadlock Detection Using Wait-for Graph


class DeadlockDetection:
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
        self.rec_stack = set()

    def detect_cycle(self, tx):
        self.visited.add(tx)
        self.rec_stack.add(tx)

        for neighbor in self.graph.get(tx, []):
            if neighbor not in self.visited:
                if self.detect_cycle(neighbor):
                    return True

            elif neighbor in self.rec_stack:
                return True

        self.rec_stack.remove(tx)
        return False

    def is_deadlock(self):
        for tx in self.graph:
            if tx not in self.visited:
                if self.detect_cycle(tx):
                    return True

        return False


graph = {
    "T1": ["T2"],
    "T2": ["T3"],
    "T3": ["T1"]
}

detector = DeadlockDetection(graph)

if detector.is_deadlock():
    print("Deadlock detected!")
else:
    print("No deadlock detected.")
