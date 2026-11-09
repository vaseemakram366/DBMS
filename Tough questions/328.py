# Resource Allocation Graph


class ResourceAllocationGraph:
    def __init__(self):
        self.graph = {
            "P1": ["R1"],
            "R1": ["P2"],
            "P2": ["R2"],
            "R2": ["P1"]
        }

    def detect_cycle(self):
        visited = set()
        path = set()

        def dfs(node):
            visited.add(node)
            path.add(node)

            for neighbor in self.graph.get(node, []):
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

    def display(self):
        print("Resource Allocation Graph:")

        for node, neighbors in self.graph.items():
            for neighbor in neighbors:
                print(f"{node} -> {neighbor}")

        if self.detect_cycle():
            print("Cycle Detected: Deadlock Possible!")
        else:
            print("No Cycle: No Deadlock Indicated.")


obj = ResourceAllocationGraph()
obj.display()
