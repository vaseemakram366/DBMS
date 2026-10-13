# Database Query Fingerprinting Engine


import re
from collections import Counter


class QueryFingerprintEngine:
    def __init__(self):
        self.query_counts = Counter()
        self.original_queries = {}

    def normalize(self, query):
        query = query.strip().lower()

        query = re.sub(
            r"'(?:''|[^'])*'",
            "?",
            query
        )

        query = re.sub(
            r"\b\d+(?:\.\d+)?\b",
            "?",
            query
        )

        query = re.sub(
            r"\s+",
            " ",
            query
        )

        query = re.sub(
            r"\bin\s*\(\s*(?:\?\s*,\s*)*\?\s*\)",
            "in (?)",
            query
        )

        return query.rstrip(";").strip()

    def fingerprint(self, query):
        normalized = self.normalize(query)
        return normalized

    def record_query(self, query):
        fp = self.fingerprint(query)

        self.query_counts[fp] += 1

        self.original_queries.setdefault(fp, [])
        self.original_queries[fp].append(query)

        return fp

    def report(self):
        print("\nQuery Workload Report")

        for fp, count in self.query_counts.most_common():
            print(f"\nFingerprint: {fp}")
            print(f"Execution count: {count}")
            print("Example:", self.original_queries[fp][0])


engine = QueryFingerprintEngine()

queries = [
    "SELECT * FROM users WHERE id = 10;",
    "SELECT * FROM users WHERE id = 25;",
    "SELECT * FROM users WHERE id = 99;",
    "SELECT * FROM products WHERE price > 500;",
    "SELECT * FROM products WHERE price > 900;",
    "SELECT * FROM users WHERE id = 10;"
]

for query in queries:
    print("Fingerprint:", engine.record_query(query))

engine.report()
