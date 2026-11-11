# Buffer Pool Replacement Using LRU


from collections import OrderedDict

class LRUBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = OrderedDict()

    def access_page(self, page):
        if page in self.buffer:
            self.buffer.move_to_end(page)
            print(f"Page {page}: Hit")
        else:
            print(f"Page {page}: Miss")

            if len(self.buffer) == self.capacity:
                removed = self.buffer.popitem(last=False)
                print("Removed page:", removed[0])

            self.buffer[page] = True

    def display(self):
        print("Buffer Pool:", list(self.buffer.keys()))


lru = LRUBuffer(3)

for page in [1, 2, 3, 1, 4]:
    lru.access_page(page)

lru.display()
