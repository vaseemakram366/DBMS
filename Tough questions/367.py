# Database Buffer Manager


class BufferManager:
    def __init__(self):
        self.buffer_pool = []

    def access_page(self, page):
        if page in self.buffer_pool:
            print(f"Page {page}: Buffer Hit")
        else:
            self.buffer_pool.append(page)
            print(f"Page {page}: Buffer Miss - Loaded")

    def display_buffer(self):
        print("Buffer Pool:", self.buffer_pool)


bm = BufferManager()

bm.access_page(1)
bm.access_page(2)
bm.access_page(1)
bm.access_page(3)

bm.display_buffer()
    