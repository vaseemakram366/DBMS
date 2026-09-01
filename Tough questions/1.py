# 1. Deadlock Detection using Wait-For Graph

from collections import defaultdict

class DeadlockDetector:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_dependency(self, process1, process2):
        self.graph[process1].append(process2)

    def detect_deadlock(self):
        visited = set()
        recursion_stack = set()

        def dfs(process):
            visited.add(process)
            recursion_stack.add(process)

            for next_process in self.graph[process]:
                if next_process not in visited:
                    if dfs(next_process):
                        return True

                elif next_process in recursion_stack:
                    return True

            recursion_stack.remove(process)
            return False

        for process in self.graph:
            if process not in visited:
                if dfs(process):
                    return True

        return False


db = DeadlockDetector()

db.add_dependency("P1", "P2")
db.add_dependency("P2", "P3")
db.add_dependency("P3", "P1")

if db.detect_deadlock():
    print("Deadlock detected")
else:
    print("No deadlock")