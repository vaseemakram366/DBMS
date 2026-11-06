# Deadlock Detection Using Wait-For Graph


class WaitForGraph:
    def __init__(self):
        self.graph = {
            "T1": ["T2"],
            "T2": ["T3"],
            "T3": []
        }

    def detect_cycle(self):
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

    def detect_deadlock(self):
        print("Wait-For Graph:", self.graph)

        if self.detect_cycle():
            print("Deadlock detected!")
        else:
            print("No deadlock detected.")


db = WaitForGraph()
db.detect_deadlock()
