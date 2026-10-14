# Query Result Cache with Dependency Tracking


from collections import defaultdict


class QueryResultCache:
    def __init__(self):
        self.cache = {}
        self.dependencies = defaultdict(set)
        self.query_tables = {}

    def put(self, query, result, tables):
        tables = set(tables)

        self.cache[query] = result
        self.query_tables[query] = tables

        for table in tables:
            self.dependencies[table].add(query)

        print(f"Cached: {query}")

    def get(self, query):
        if query in self.cache:
            print(f"Cache HIT: {query}")
            return self.cache[query]

        print(f"Cache MISS: {query}")
        return None

    def invalidate_table(self, table):
        affected_queries = self.dependencies.pop(
            table, set()
        )

        for query in affected_queries:
            self.cache.pop(query, None)

            for dependency in self.query_tables.get(query, set()):
                self.dependencies[dependency].discard(query)

            self.query_tables.pop(query, None)

        print(
            f"Invalidated {len(affected_queries)} "
            f"cached queries for table '{table}'"
        )

    def show_cache(self):
        print("\nCurrent cached queries:")
        for query, result in self.cache.items():
            print(query, "->", result)


cache = QueryResultCache()

q1 = "SELECT * FROM employees"
q2 = "SELECT name FROM employees WHERE salary > 50000"
q3 = "SELECT * FROM departments"

cache.put(
    q1,
    [{"id": 1, "name": "Aman"}],
    ["employees"]
)

cache.put(
    q2,
    [{"name": "Riya"}],
    ["employees"]
)

cache.put(
    q3,
    [{"id": 1, "name": "IT"}],
    ["departments"]
)

print("\nFirst request:")
print(cache.get(q1))

print("\nUpdate employees table:")
cache.invalidate_table("employees")

print("\nRequest after update:")
print(cache.get(q1))
print(cache.get(q3))

cache.show_cache()
