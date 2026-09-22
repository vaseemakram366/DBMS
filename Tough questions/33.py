# Query Result Cache with LRU + TTL

import time
from collections import OrderedDict


class QueryCache:
    def __init__(self, capacity=3, ttl=10):
        self.capacity = capacity
        self.ttl = ttl
        self.cache = OrderedDict()

    def get(self, query):
        if query not in self.cache:
            return None

        result, created_at = self.cache[query]

        if time.time() - created_at > self.ttl:
            del self.cache[query]
            return None

        self.cache.move_to_end(query)

        return result

    def put(self, query, result):
        if query in self.cache:
            del self.cache[query]

        self.cache[query] = (
            result,
            time.time()
        )

        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def invalidate(self, query=None):
        if query is None:
            self.cache.clear()
        elif query in self.cache:
            del self.cache[query]

    def show(self):
        for query, (result, created_at) in self.cache.items():
            age = round(time.time() - created_at, 2)
            print(
                f"Query: {query} | "
                f"Result: {result} | "
                f"Age: {age}s"
            )


class Database:
    def __init__(self):
        self.cache = QueryCache(
            capacity=3,
            ttl=5
        )

    def execute(self, query):
        cached = self.cache.get(query)

        if cached is not None:
            print("CACHE HIT")
            return cached

        print("CACHE MISS")

        result = self.run_query(query)

        self.cache.put(query, result)

        return result

    def run_query(self, query):
        time.sleep(0.5)

        if "employees" in query:
            return [
                (1, "Amit"),
                (2, "Rahul"),
                (3, "Vaseem")
            ]

        return []


db = Database()

query = "SELECT * FROM employees"

print(db.execute(query))
print(db.execute(query))

print("\nCache:")
db.cache.show()

db.cache.invalidate(query)

print("\nAfter invalidation:")
print(db.execute(query))