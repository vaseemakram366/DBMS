# Deadlock Prevention and Victim Selection Simulator


class DeadlockResolver:
    def __init__(self):
        self.graph = {}
        self.cost = {}
        self.active = set()

    def add_transaction(self, tid, rollback_cost):
        self.graph.setdefault(tid, [])
        self.cost[tid] = rollback_cost
        self.active.add(tid)

    def add_wait(self, waiting, blocking):
        self.graph[waiting].append(blocking)
        print(f"{waiting} waits for {blocking}")

    def find_cycle(self):
        visited = set()
        path = []
        active_path = set()

        def dfs(node):
            visited.add(node)
            path.append(node)
            active_path.add(node)

            for neighbor in self.graph[node]:
                if neighbor not in visited:
                    cycle = dfs(neighbor)
                    if cycle:
                        return cycle
                elif neighbor in active_path:
                    start = path.index(neighbor)
                    return path[start:]

            path.pop()
            active_path.remove(node)
            return None

        for node in self.graph:
            if node not in visited:
                cycle = dfs(node)
                if cycle:
                    return cycle

        return None

    def resolve(self):
        cycle = self.find_cycle()

        if not cycle:
            print("No deadlock detected.")
            return

        print("Deadlock cycle:", " -> ".join(cycle + [cycle[0]]))

        victim = min(cycle, key=lambda tid: self.cost[tid])

        print(f"Victim selected: {victim}")
        print(f"Rollback cost: {self.cost[victim]}")

        self.active.remove(victim)
        self.graph.pop(victim)

        for tid in self.graph:
            self.graph[tid] = [
                neighbor
                for neighbor in self.graph[tid]
                if neighbor != victim
            ]

        print(f"{victim} aborted; its resources are released.")
        print("Remaining active transactions:", sorted(self.active))


db = DeadlockResolver()

db.add_transaction("T1", 8)
db.add_transaction("T2", 3)
db.add_transaction("T3", 6)

db.add_wait("T1", "T2")
db.add_wait("T2", "T3")
db.add_wait("T3", "T1")

db.resolve()
