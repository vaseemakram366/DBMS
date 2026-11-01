# LRU Page Replacement Simulator


class LRUSimulator:
    def __init__(self, capacity):
        self.capacity = capacity
        self.pages = []

    def access_page(self, page_id):
        if page_id in self.pages:
            self.pages.remove(page_id)
            self.pages.append(page_id)
            print(f"Page {page_id}: HIT")
        else:
            print(f"Page {page_id}: MISS")

            if len(self.pages) == self.capacity:
                removed = self.pages.pop(0)
                print(f"Evicted page {removed}")

            self.pages.append(page_id)
            print(f"Loaded page {page_id}")

    def show_pages(self):
        print("Pages (LRU to MRU):", self.pages)


lru = LRUSimulator(3)

lru.access_page(1)
lru.access_page(2)
lru.access_page(3)
lru.access_page(1)
lru.access_page(4)

lru.show_pages()
