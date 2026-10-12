# Adaptive Replacement Cache (ARC)


from collections import OrderedDict


class ARCCache:
    def __init__(self, capacity):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")

        self.capacity = capacity
        self.p = 0

        self.T1 = OrderedDict()
        self.T2 = OrderedDict()
        self.B1 = OrderedDict()
        self.B2 = OrderedDict()

    def replace(self, page):
        if self.T1 and (
            len(self.T1) > self.p
            or (page in self.B2 and len(self.T1) == self.p)
        ):
            old, _ = self.T1.popitem(last=False)
            self.B1[old] = None
        elif self.T2:
            old, _ = self.T2.popitem(last=False)
            self.B2[old] = None

    def access(self, page):
        if page in self.T1:
            value = self.T1.pop(page)
            self.T2[page] = value
            return "Cache hit"

        if page in self.T2:
            value = self.T2.pop(page)
            self.T2[page] = value
            return "Cache hit"

        if page in self.B1:
            delta = max(1, len(self.B2) // max(1, len(self.B1)))
            self.p = min(self.capacity, self.p + delta)
            self.replace(page)
            self.B1.pop(page)
            self.T2[page] = page
            return "Cache miss"

        if page in self.B2:
            delta = max(1, len(self.B1) // max(1, len(self.B2)))
            self.p = max(0, self.p - delta)
            self.replace(page)
            self.B2.pop(page)
            self.T2[page] = page
            return "Cache miss"

        if len(self.T1) + len(self.B1) == self.capacity:
            if len(self.T1) < self.capacity:
                if self.B1:
                    self.B1.popitem(last=False)
                self.replace(page)
            else:
                if self.T1:
                    self.T1.popitem(last=False)
        elif (
            len(self.T1) + len(self.T2)
            + len(self.B1) + len(self.B2)
            >= self.capacity
        ):
            if (
                len(self.T1) + len(self.T2)
                + len(self.B1) + len(self.B2)
                == 2 * self.capacity
            ):
                if self.B2:
                    self.B2.popitem(last=False)
            self.replace(page)

        self.T1[page] = page
        return "Cache miss"

    def show(self):
        print("T1 (recent pages):", list(self.T1.keys()))
        print("T2 (frequent pages):", list(self.T2.keys()))
        print("B1 (recent evictions):", list(self.B1.keys()))
        print("B2 (frequent evictions):", list(self.B2.keys()))
        print("Adaptive target p:", self.p)


cache = ARCCache(3)

for page in [1, 2, 3, 1, 2, 4, 1, 2, 5]:
    print(f"Page {page}: {cache.access(page)}")

print("\nFinal cache state:")
cache.show()
