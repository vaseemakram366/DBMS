# Database Frequency Estimator


import hashlib


class CountMinSketch:
    def __init__(self, width=100, depth=5):
        self.width = width
        self.depth = depth
        self.table = [
            [0] * width for _ in range(depth)
        ]

    def _hash(self, value, seed):
        data = f"{seed}:{value}".encode()
        digest = hashlib.sha256(data).hexdigest()
        return int(digest, 16) % self.width

    def add(self, value, count=1):
        for i in range(self.depth):
            index = self._hash(value, i)
            self.table[i][index] += count

    def estimate(self, value):
        estimates = []

        for i in range(self.depth):
            index = self._hash(value, i)
            estimates.append(self.table[i][index])

        return min(estimates)


class DatabaseAnalytics:
    def __init__(self):
        self.sketch = CountMinSketch(width=200, depth=5)

    def record_search(self, product):
        self.sketch.add(product)

    def estimated_searches(self, product):
        return self.sketch.estimate(product)


db = DatabaseAnalytics()

searches = [
    "Laptop", "Phone", "Laptop", "Tablet",
    "Laptop", "Phone", "Laptop", "Headphones",
    "Phone", "Laptop", "Tablet", "Laptop"
]

for product in searches:
    db.record_search(product)

for product in ["Laptop", "Phone", "Tablet", "Headphones"]:
    print(product, ":", db.estimated_searches(product))