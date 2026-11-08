# Deadlock Detection Using Resource Allocation Graph


class ResourceAllocationGraph:
    def __init__(self):
        self.graph = {
            "T1": ["R1"],
            "R1": ["T2"],
            "T2": ["R2"],
            "R2": ["T1"]
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
        print("Resource Allocation Graph:", self.graph)

        if self.detect_cycle():
            print("Deadlock Detected!")
        else:
            print("No Deadlock Detected")


rag = ResourceAllocationGraph()
rag.detect_deadlock()
