# LRU Buffer Replacement Policy


class LRUBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = []  # Oldest to newest

    def access(self, page):
        if page in self.pages:
            self.pages.remove(page)
            self.pages.append(page)
            print(f"Page {page}: hit")
        else:
            print(f"Page {page}: miss")

            if len(self.pages) == self.capacity:
                evicted = self.pages.pop(0)
                print(f"Evicted page {evicted}")

            self.pages.append(page)

    def show(self):
        print("LRU order (oldest to newest):", self.pages)


buffer = LRUBuffer(3)

for page in [1, 2, 3, 1, 4, 2, 5]:
    buffer.access(page)

buffer.show()
