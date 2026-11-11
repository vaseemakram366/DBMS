# Buffer Pool Replacement Using FIFO


from collections import deque

class FIFOBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = deque()
        self.pages = set()

    def access_page(self, page):
        if page in self.pages:
            print(f"Page {page}: Hit")
        else:
            print(f"Page {page}: Miss")

            if len(self.buffer) == self.capacity:
                removed = self.buffer.popleft()
                self.pages.remove(removed)
                print("Removed page:", removed)

            self.buffer.append(page)
            self.pages.add(page)

    def display(self):
        print("Buffer Pool:", list(self.buffer))


fifo = FIFOBuffer(3)

for page in [1, 2, 3, 4, 2]:
    fifo.access_page(page)

fifo.display()
