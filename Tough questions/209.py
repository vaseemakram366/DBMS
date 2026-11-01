# LFU Page Replacement Simulator


class LFUSimulator:
    def __init__(self, capacity):
        self.capacity = capacity
        self.frequency = {}
        self.last_used = {}
        self.time = 0

    def access_page(self, page_id):
        self.time += 1

        if page_id in self.frequency:
            self.frequency[page_id] += 1
            self.last_used[page_id] = self.time

            print(
                f"Page {page_id}: HIT, "
                f"frequency = {self.frequency[page_id]}"
            )
            return

        print(f"Page {page_id}: MISS")

        if len(self.frequency) == self.capacity:
            removed = min(
                self.frequency,
                key=lambda p: (
                    self.frequency[p],
                    self.last_used[p]
                )
            )

            print(f"Evicted page {removed}")

            del self.frequency[removed]
            del self.last_used[removed]

        self.frequency[page_id] = 1
        self.last_used[page_id] = self.time

        print(f"Loaded page {page_id}, frequency = 1")

    def show_pages(self):
        print("Page frequencies:", dict(sorted(self.frequency.items())))


lfu = LFUSimulator(3)

lfu.access_page(1)
lfu.access_page(2)
lfu.access_page(3)
lfu.access_page(1)
lfu.access_page(4)

lfu.show_pages()
