# Buffer Pool Replacement Using LFU


from collections import OrderedDict

class LFUBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = OrderedDict()

    def access_page(self, page):
        if page in self.buffer:
            self.buffer[page] += 1
            print(f"Page {page}: Hit (frequency={self.buffer[page]})")
        else:
            print(f"Page {page}: Miss")

            if len(self.buffer) == self.capacity:
                victim = min(self.buffer, key=self.buffer.get)
                del self.buffer[victim]
                print("Removed page:", victim)

            self.buffer[page] = 1

    def display(self):
        print("Buffer Pool:", dict(self.buffer))


lfu = LFUBuffer(3)

for page in [1, 2, 1, 3, 2, 4]:
    lfu.access_page(page)

lfu.display()
