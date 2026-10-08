# Query Admission Control / Workload Manager

import heapq
import time


class Query:
    def __init__(self, query_id, sql, priority, memory):
        self.query_id = query_id
        self.sql = sql
        self.priority = priority
        self.memory = memory
        self.created_at = time.time()

    def __lt__(self, other):
        return self.priority > other.priority


class QueryAdmissionController:
    def __init__(self, max_concurrent=3, memory_limit=1000):
        self.max_concurrent = max_concurrent
        self.memory_limit = memory_limit

        self.running = []
        self.waiting = []

        self.used_memory = 0

    def submit(self, query):
        if (
            len(self.running) < self.max_concurrent
            and self.used_memory + query.memory <= self.memory_limit
        ):
            self._start(query)
            return "RUNNING"

        heapq.heappush(self.waiting, query)
        return "QUEUED"

    def _start(self, query):
        self.running.append(query)
        self.used_memory += query.memory

    def finish(self, query_id):
        for i, query in enumerate(self.running):
            if query.query_id == query_id:
                self.running.pop(i)
                self.used_memory -= query.memory
                break

        self._schedule()

    def _schedule(self):
        while self.waiting:
            if len(self.running) >= self.max_concurrent:
                break

            selected = None

            for query in self.waiting:
                if (
                    self.used_memory + query.memory
                    <= self.memory_limit
                ):
                    selected = query
                    break

            if selected is None:
                break

            self.waiting.remove(selected)
            heapq.heapify(self.waiting)

            self._start(selected)

    def status(self):
        print("Running queries:")

        for query in self.running:
            print(
                query.query_id,
                "| priority:",
                query.priority,
                "| memory:",
                query.memory
            )

        print("Queued queries:", len(self.waiting))
        print("Used memory:", self.used_memory)


manager = QueryAdmissionController(
    max_concurrent=2,
    memory_limit=1000
)

queries = [
    Query(1, "SELECT * FROM users", 2, 300),
    Query(2, "SELECT * FROM orders", 5, 400),
    Query(3, "SELECT * FROM products", 1, 500),
    Query(4, "SELECT * FROM payments", 10, 300),
]

for query in queries:
    print(
        f"Query {query.query_id}:",
        manager.submit(query)
    )

print("\nInitial state:")
manager.status()

manager.finish(1)

print("\nAfter Query 1 finishes:")
manager.status()