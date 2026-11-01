# Database Buffer Pool Manager


class BufferPoolManager:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = []

    def access_page(self, page_id):
        if page_id in self.pages:
            print(f"Page {page_id}: BUFFER HIT")
            return

        print(f"Page {page_id}: BUFFER MISS")

        if len(self.pages) == self.capacity:
            removed = self.pages.pop(0)
            print(f"Evicted page {removed}")

        self.pages.append(page_id)
        print(f"Loaded page {page_id}")

    def show_buffer(self):
        print("Buffer pool:", self.pages)


buffer = BufferPoolManager(3)

buffer.access_page(1)
buffer.access_page(2)
buffer.access_page(3)
buffer.access_page(2)
buffer.access_page(4)

buffer.show_buffer()
