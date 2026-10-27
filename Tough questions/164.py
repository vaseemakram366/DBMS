# Incremental Cycle Detector


from collections import defaultdict, deque


class IncrementalCycleDetector:
    def __init__(self):
        self.graph = defaultdict(set)
        self.transactions = set()

    def has_cycle(self):
        indegree = {t: 0 for t in self.transactions}

        for source in self.graph:
            for target in self.graph[source]:
                indegree[target] += 1

        queue = deque(
            t for t in self.transactions if indegree[t] == 0
        )

        processed = 0

        while queue:
            current = queue.popleft()
            processed += 1

            for neighbor in self.graph[current]:
                indegree[neighbor] -= 1

                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        return processed != len(self.transactions)

    def add_edge(self, source, target):
        self.transactions.update([source, target])
        self.graph[source]
        self.graph[target]

        if source == target:
            print(f"Edge T{source} -> T{target}: cycle detected!")
            return True

        if target in self.graph[source]:
            print(f"Edge T{source} -> T{target}: already exists.")
            return self.has_cycle()

        self.graph[source].add(target)
        cycle_found = self.has_cycle()

        status = "CYCLE DETECTED" if cycle_found else "No cycle"
        print(f"Added T{source} -> T{target}: {status}")

        return cycle_found

    def display_graph(self):
        return {
            t: sorted(self.graph[t])
            for t in sorted(self.transactions)
        }


if __name__ == "__main__":
    detector = IncrementalCycleDetector()

    edges = [
        (1, 2),
        (2, 3),
        (3, 4),
        (4, 2),
    ]

    for source, target in edges:
        detector.add_edge(source, target)
        print("Current graph:", detector.display_graph())
        print()

    if detector.has_cycle():
        print("Result: NOT conflict-serializable")
    else:
        print("Result: Conflict-serializable")
