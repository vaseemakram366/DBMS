# Distributed Deadlock Detection


class DeadlockDetection:
    def __init__(self):
        self.graph = {
            "T1": ["T2"],
            "T2": ["T3"],
            "T3": ["T1"]
        }

    def detect_cycle(self, node, visited, path):
        visited.add(node)
        path.add(node)

        for neighbor in self.graph.get(node, []):
            if neighbor not in visited:
                if self.detect_cycle(neighbor, visited, path):
                    return True
            elif neighbor in path:
                return True

        path.remove(node)
        return False

    def detect_deadlock(self):
        visited = set()

        for node in self.graph:
            if node not in visited:
                if self.detect_cycle(node, visited, set()):
                    print("Deadlock detected!")
                    return

        print("No deadlock detected.")


db = DeadlockDetection()
db.detect_deadlock()
