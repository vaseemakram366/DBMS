# Database Buffer Pool Simulator


class BufferPool:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = []

    def access_page(self, page_id):
        if page_id in self.pages:
            print(f"Page {page_id}: buffer hit")
            return

        print(f"Page {page_id}: buffer miss")

        if len(self.pages) == self.capacity:
            evicted = self.pages.pop(0)
            print(f"Evicted page {evicted}")

        self.pages.append(page_id)

    def show(self):
        print("Buffer pool:", self.pages)


pool = BufferPool(3)

for page in [1, 2, 3, 2, 4]:
    pool.access_page(page)

pool.show()
