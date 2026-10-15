# Database Buffer Pool Hit-Ratio Analyzer


from collections import OrderedDict


class BufferPoolAnalyzer:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.pool = OrderedDict()
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def access_page(self, page_id):
        if page_id in self.pool:
            self.hits += 1
            self.pool.move_to_end(page_id)
            print(f"Page {page_id}: CACHE HIT")
            return

        self.misses += 1
        print(f"Page {page_id}: CACHE MISS - Read from disk")

        if len(self.pool) == self.capacity:
            removed_page, _ = self.pool.popitem(last=False)
            self.evictions += 1
            print(f"  Evicted page {removed_page} (LRU)")

        self.pool[page_id] = True

    def report(self):
        total = self.hits + self.misses
        hit_ratio = self.hits / total * 100 if total else 0
        miss_ratio = self.misses / total * 100 if total else 0

        print("\n===== Buffer Pool Report =====")
        print(f"Total requests: {total}")
        print(f"Cache hits: {self.hits}")
        print(f"Cache misses: {self.misses}")
        print(f"Evictions: {self.evictions}")
        print(f"Hit ratio: {hit_ratio:.2f}%")
        print(f"Miss ratio: {miss_ratio:.2f}%")
        print(f"Pages in memory: {list(self.pool.keys())}")


analyzer = BufferPoolAnalyzer(capacity=3)

requests = [1, 2, 3, 1, 4, 2, 5, 1]

for page_id in requests:
    analyzer.access_page(page_id)

analyzer.report()
