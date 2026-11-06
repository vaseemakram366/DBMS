# Precedence Graph Construction


class PrecedenceGraph:
    def __init__(self):
        self.schedule = [
            ("T1", "WRITE", "A"),
            ("T2", "READ", "A"),
            ("T2", "WRITE", "B"),
            ("T3", "READ", "B")
        ]

    def construct_graph(self):
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

        print("Precedence Graph:")

        for transaction in graph:
            edges = sorted(graph[transaction])
            print(f"{transaction} -> {edges}")


pg = PrecedenceGraph()
pg.construct_graph()
