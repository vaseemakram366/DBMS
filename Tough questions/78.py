# Database Query Plan Cache

import time
from collections import OrderedDict


class QueryPlan:
    def __init__(self, query, plan):
        self.query = query
        self.plan = plan
        self.created_at = time.time()
        self.execution_count = 0

    def execute(self):
        self.execution_count += 1

        print(
            f"Executing plan: {self.plan}"
        )


class QueryPlanCache:
    def __init__(self, capacity=3, ttl=60):
        self.capacity = capacity
        self.ttl = ttl
        self.cache = OrderedDict()

    def normalize(self, query):
        return " ".join(query.lower().split())

    def get(self, query):
        key = self.normalize(query)

        if key not in self.cache:
            return None

        plan = self.cache[key]

        if time.time() - plan.created_at > self.ttl:
            del self.cache[key]
            return None

        self.cache.move_to_end(key)

        return plan

    def put(self, query, plan):
        key = self.normalize(query)

        if key in self.cache:
            del self.cache[key]

        if len(self.cache) >= self.capacity:
            self.cache.popitem(last=False)

        self.cache[key] = QueryPlan(
            query,
            plan
        )

    def invalidate(self, query):
        key = self.normalize(query)

        if key in self.cache:
            del self.cache[key]

    def clear(self):
        self.cache.clear()

    def display(self):
        print("\nPlan Cache:")

        for key, plan in self.cache.items():
            print(
                f"Query: {key}\n"
                f"Plan: {plan.plan}\n"
                f"Executions: {plan.execution_count}\n"
            )


class QueryEngine:
    def __init__(self):
        self.cache = QueryPlanCache()

    def optimize(self, query):
        print("Optimizing query...")

        if "where" in query.lower():
            return "INDEX_SCAN"
        return "FULL_TABLE_SCAN"

    def execute(self, query):
        plan = self.cache.get(query)

        if plan:
            print("CACHE HIT")
            plan.execute()
            return

        print("CACHE MISS")

        optimized_plan = self.optimize(query)

        self.cache.put(
            query,
            optimized_plan
        )

        plan = self.cache.get(query)

        plan.execute()


engine = QueryEngine()

query = """
SELECT name
FROM employees
WHERE salary > 50000
"""

engine.execute(query)

engine.execute(query)

engine.execute(query)

engine.cache.display()