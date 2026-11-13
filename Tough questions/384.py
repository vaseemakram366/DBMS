# Slotted Page Space Management


class SlottedPage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.used_space = 0
        self.records = []

    def insert_record(self, record, size):
        if self.used_space + size <= self.capacity:
            self.records.append((record, size))
            self.used_space += size
            print(f"{record} inserted")
        else:
            print("Not enough space")

    def display_space(self):
        free_space = self.capacity - self.used_space

        print("Total Space:", self.capacity)
        print("Used Space:", self.used_space)
        print("Free Space:", free_space)


page = SlottedPage(100)

page.insert_record("Alice", 20)
page.insert_record("Bob", 30)
page.insert_record("Charlie", 25)
page.insert_record("David", 40)

page.display_space()
