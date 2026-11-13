# Slotted Page Structure


class SlottedPage:
    def __init__(self):
        self.records = []
        self.slots = []

    def insert_record(self, record):
        offset = len(self.records)
        self.records.append(record)
        self.slots.append(offset)

        print(f"Record inserted at slot {len(self.slots) - 1}")

    def get_record(self, slot):
        if 0 <= slot < len(self.slots):
            offset = self.slots[slot]
            return self.records[offset]

        return "Invalid slot"

    def display(self):
        print("Records:", self.records)
        print("Slot Directory:", self.slots)


page = SlottedPage()

page.insert_record("Alice")
page.insert_record("Bob")
page.insert_record("Charlie")

print("Record at slot 1:", page.get_record(1))

page.display()
