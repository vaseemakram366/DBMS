# Record Insertion in Slotted Page


class SlottedPage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.used_space = 0
        self.records = []
        self.slots = []

    def insert_record(self, record, size):
        if self.used_space + size > self.capacity:
            print("Page is full")
            return

        self.records.append(record)
        self.slots.append(len(self.records) - 1)
        self.used_space += size

        print(f"Inserted {record} at slot {len(self.slots) - 1}")

    def display(self):
        print("Records:", self.records)
        print("Slot Directory:", self.slots)
        print("Used Space:", self.used_space)


page = SlottedPage(100)

page.insert_record("Alice", 20)
page.insert_record("Bob", 25)
page.insert_record("Charlie", 30)
page.insert_record("David", 40)

page.display()
