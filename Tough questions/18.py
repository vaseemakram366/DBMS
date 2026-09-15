# Buffer Manager with LRU Page Replacement
from collections import OrderedDict


class BufferManager:

    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = OrderedDict()
        self.dirty_pages = set()
        self.hits = 0
        self.misses = 0

    def read_page(self, page_id):
        if page_id in self.buffer:
            self.hits += 1
            self.buffer.move_to_end(page_id)
            print("READ", page_id, "-> HIT")
            return

        self.misses += 1
        print("READ", page_id, "-> MISS")

        self.load_page(page_id)

    def load_page(self, page_id):
        if len(self.buffer) >= self.capacity:
            self.evict_page()

        self.buffer[page_id] = f"Data for Page {page_id}"

        print("Loaded Page:", page_id)

    def write_page(self, page_id, data):
        if page_id not in self.buffer:
            self.load_page(page_id)

        self.buffer[page_id] = data
        self.dirty_pages.add(page_id)

        self.buffer.move_to_end(page_id)

        print("WRITE", page_id, "-> DIRTY")

    def evict_page(self):
        page_id, data = self.buffer.popitem(last=False)

        if page_id in self.dirty_pages:
            print(
                "Writing dirty Page",
                page_id,
                "to disk"
            )

            self.dirty_pages.remove(page_id)

        print("Evicted Page:", page_id)

    def flush(self):
        print("\nFlushing dirty pages...")

        for page_id in list(self.dirty_pages):
            print(
                "Writing Page",
                page_id,
                "to disk"
            )

        self.dirty_pages.clear()

    def display(self):
        print("\nBuffer Pool:")

        for page_id, data in self.buffer.items():
            status = "DIRTY" if page_id in self.dirty_pages else "CLEAN"
            print(page_id, "->", data, "->", status)

        print("\nHits:", self.hits)
        print("Misses:", self.misses)


buffer = BufferManager(3)

buffer.read_page(1)
buffer.read_page(2)
buffer.read_page(3)

buffer.read_page(1)

buffer.write_page(2, "Updated Data")

buffer.read_page(4)

buffer.read_page(5)

buffer.display()

buffer.flush()

buffer.display()