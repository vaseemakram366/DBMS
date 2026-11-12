# Buffer Pool Pinning and Unpinning


class BufferPool:
    def __init__(self):
        self.buffer = {}

    def load_page(self, page):
        self.buffer[page] = {"pin_count": 0}
        print(f"Page {page} loaded")

    def pin_page(self, page):
        if page in self.buffer:
            self.buffer[page]["pin_count"] += 1
            print(f"Page {page} pinned")

    def unpin_page(self, page):
        if page in self.buffer and self.buffer[page]["pin_count"] > 0:
            self.buffer[page]["pin_count"] -= 1
            print(f"Page {page} unpinned")

    def display(self):
        for page, info in self.buffer.items():
            print(f"Page {page}: Pin Count = {info['pin_count']}")


pool = BufferPool()

pool.load_page(1)
pool.load_page(2)

pool.pin_page(1)
pool.pin_page(1)

pool.unpin_page(1)

pool.display()
