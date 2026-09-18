# Deadlock Detection using Resource Allocation Graph

from collections import defaultdict


class ResourceAllocationGraph:

    def __init__(self):
        self.processes = set()
        self.resources = set()
        self.allocation = defaultdict(list)
        self.request = defaultdict(list)

    def add_process(self, process):
        self.processes.add(process)

    def add_resource(self, resource):
        self.resources.add(resource)

    def allocate(self, resource, process):
        self.allocation[resource].append(process)

    def request_resource(self, process, resource):
        self.request[process].append(resource)

    def build_graph(self):
        graph = defaultdict(list)

        for process in self.processes:

            for resource in self.request[process]:

                for holder in self.allocation[resource]:
                    graph[process].append(holder)

        return graph

    def detect_deadlock(self):
        graph = self.build_graph()

        visited = set()
        path = set()

        def dfs(process):

            visited.add(process)
            path.add(process)

            for next_process in graph[process]:

                if next_process not in visited:
                    if dfs(next_process):
                        return True

                elif next_process in path:
                    return True

            path.remove(process)
            return False

        for process in self.processes:

            if process not in visited:
                if dfs(process):
                    return True

        return False

    def display(self):

        graph = self.build_graph()

        print("\nResource Allocation Graph:")

        for process in graph:

            for holder in graph[process]:

                print(
                    process,
                    "->",
                    holder
                )


rag = ResourceAllocationGraph()

rag.add_process("P1")
rag.add_process("P2")
rag.add_process("P3")

rag.add_resource("R1")
rag.add_resource("R2")
rag.add_resource("R3")

rag.allocate("R1", "P1")
rag.allocate("R2", "P2")
rag.allocate("R3", "P3")

rag.request_resource("P1", "R2")
rag.request_resource("P2", "R3")
rag.request_resource("P3", "R1")

rag.display()

if rag.detect_deadlock():
    print("\nDEADLOCK DETECTED")
else:
    print("\nNO DEADLOCK")