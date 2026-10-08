# Query Admission Control with Fair Scheduling

import heapq


class Query:
    def __init__(self, query_id, user, priority, cost):
        self.query_id = query_id
        self.user = user
        self.priority = priority
        self.cost = cost

    def __lt__(self, other):
        return self.priority > other.priority


class FairQueryScheduler:
    def __init__(self, max_slots=2):
        self.max_slots = max_slots
        self.running = []
        self.queue = []

    def submit(self, query):
        heapq.heappush(self.queue, query)
        self.schedule()

    def schedule(self):
        while (
            len(self.running) < self.max_slots
            and self.queue
        ):
            query = heapq.heappop(self.queue)

            self.running.append(query)

            print(
                f"Started Query {query.query_id} "
                f"from {query.user}"
            )

    def finish(self, query_id):
        for i, query in enumerate(self.running):
            if query.query_id == query_id:
                finished = self.running.pop(i)

                print(
                    f"Finished Query {finished.query_id}"
                )

                break

        self.schedule()

    def status(self):
        print("\nRunning:")

        for query in self.running:
            print(
                f"Q{query.query_id} "
                f"| User={query.user} "
                f"| Priority={query.priority}"
            )

        print("Waiting:", len(self.queue))


scheduler = FairQueryScheduler(max_slots=2)

scheduler.submit(
    Query(1, "Alice", 2, 100)
)

scheduler.submit(
    Query(2, "Bob", 5, 200)
)

scheduler.submit(
    Query(3, "Charlie", 10, 300)
)

scheduler.submit(
    Query(4, "Alice", 1, 150)
)

scheduler.status()

print("\nCompleting Query 1...")
scheduler.finish(1)

scheduler.status()

print("\nCompleting Query 2...")
scheduler.finish(2)

scheduler.status()