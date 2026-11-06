# Conflict Serializability Checker


class ConflictSerializability:
    def __init__(self):
        self.schedule = [
            ("T1", "WRITE", "A"),
            ("T2", "READ", "A"),
            ("T1", "READ", "B"),
            ("T2", "WRITE", "B")
        ]

    def check(self):
        graph = {}

        for transaction, operation, data in self.schedule:
            graph.setdefault(transaction, set())

        n = len(self.schedule)

        for i in range(n):
            t1, op1, data1 = self.schedule[i]

            for j in range(i + 1, n):
                t2, op2, data2 = self.schedule[j]

                if t1 != t2 and data1 == data2:
                    if op1 == "WRITE" or op2 == "WRITE":
                        graph[t1].add(t2)

        visited = set()
        active = set()

        def has_cycle(node):
            visited.add(node)
            active.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    if has_cycle(neighbor):
                        return True
                elif neighbor in active:
                    return True

            active.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if has_cycle(node):
                    print("Schedule is NOT Conflict Serializable")
                    return

        print("Schedule is Conflict Serializable")
        print("Precedence Graph:", graph)


checker = ConflictSerializability()
checker.check()
