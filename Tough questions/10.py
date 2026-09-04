# LRU Buffer Pool
from collections import OrderedDict


class BufferPool:

    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = OrderedDict()

        self.hits = 0
        self.misses = 0

    def access_page(self, page):

        if page in self.pages:

            self.hits += 1

            # Move recently used page to end
            self.pages.move_to_end(page)

            print("Page", page, "-> HIT")

        else:

            self.misses += 1

            print("Page", page, "-> MISS")

            if len(self.pages) >= self.capacity:

                removed = self.pages.popitem(
                    last=False
                )

                print(
                    "Evicted page:",
                    removed[0]
                )

            self.pages[page] = True

    def show(self):

        print("\nBuffer Pool:")

        for page in self.pages:
            print(page, end=" ")

        print()

        print("Hits:", self.hits)
        print("Misses:", self.misses)


buffer = BufferPool(3)

pages = [1, 2, 3, 1, 4, 2, 5, 1]

for page in pages:
    buffer.access_page(page)

buffer.show()