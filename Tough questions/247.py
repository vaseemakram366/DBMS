# Buffer Pool Pin and Unpin Management


class BufferPool:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = []
        self.pin_count = {}

    def pin_page(self, page_id):
        if page_id not in self.pages:
            if len(self.pages) == self.capacity:
                unpinned = [
                    p for p in self.pages
                    if self.pin_count[p] == 0
                ]

                if not unpinned:
                    print("Cannot load page: all pages are pinned")
                    return

                evicted = unpinned[0]
                self.pages.remove(evicted)
                del self.pin_count[evicted]
                print(f"Evicted page {evicted}")

            self.pages.append(page_id)
            self.pin_count[page_id] = 0
            print(f"Loaded page {page_id}")

        self.pin_count[page_id] += 1
        print(f"Page {page_id} pinned: count = {self.pin_count[page_id]}")

    def unpin_page(self, page_id):
        if page_id not in self.pages or self.pin_count[page_id] == 0:
            print(f"Page {page_id} is not pinned")
            return

        self.pin_count[page_id] -= 1
        print(f"Page {page_id} unpinned: count = {self.pin_count[page_id]}")

    def show(self):
        print("Buffer pages:", self.pages)
        print("Pin counts:", self.pin_count)


pool = BufferPool(2)

pool.pin_page(1)
pool.pin_page(2)
pool.pin_page(3)
pool.unpin_page(1)
pool.pin_page(3)
pool.show()
