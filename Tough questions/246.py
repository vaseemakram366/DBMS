# LFU Buffer Replacement Policy


class LFUBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = []
        self.frequency = {}
        self.order = {}

    def access(self, page):
        if page in self.pages:
            self.frequency[page] += 1
            print(f"Page {page}: hit, frequency = {self.frequency[page]}")
            return

        print(f"Page {page}: miss")

        if len(self.pages) == self.capacity:
            evicted = min(
                self.pages,
                key=lambda p: (self.frequency[p], self.order[p])
            )

            self.pages.remove(evicted)
            del self.frequency[evicted]
            del self.order[evicted]

            print(f"Evicted page {evicted}")

        self.pages.append(page)
        self.frequency[page] = 1
        self.order[page] = page

    def show(self):
        print("Buffer pages:", self.pages)
        print("Frequencies:", self.frequency)


buffer = LFUBuffer(3)

for page in [1, 2, 1, 3, 2, 4]:
    buffer.access(page)

buffer.show()
