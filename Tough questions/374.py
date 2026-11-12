# Page Replacement with Pin Count


class BufferPool:
    def __init__(self, capacity):
        self.capacity = capacity
        self.buffer = {}

    def add_page(self, page):
        if page in self.buffer:
            print(f"Page {page} already exists")
            return

        if len(self.buffer) == self.capacity:
            victim = None

            for old_page, pin_count in self.buffer.items():
                if pin_count == 0:
                    victim = old_page
                    break

            if victim is None:
                print("No replaceable page available")
                return

            del self.buffer[victim]
            print("Removed page:", victim)

        self.buffer[page] = 0
        print(f"Page {page} added")

    def pin_page(self, page):
        if page in self.buffer:
            self.buffer[page] += 1

    def display(self):
        print("Buffer Pool:", self.buffer)


pool = BufferPool(2)

pool.add_page(1)
pool.add_page(2)

pool.pin_page(1)

pool.add_page(3)

pool.display()
