# Page Fragmentation Simulation


class DatabasePage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.used = 0

    def insert_record(self, size):
        if self.used + size <= self.capacity:
            self.used += size
            print(f"Inserted record of size {size}")
        else:
            print("Not enough space")

    def display(self):
        free = self.capacity - self.used
        print("Total Capacity:", self.capacity)
        print("Used Space:", self.used)
        print("Free Space:", free)
        print("Fragmentation:", free / self.capacity * 100, "%")


page = DatabasePage(100)

page.insert_record(30)
page.insert_record(25)
page.insert_record(20)

page.display()
