# Record Deletion in Slotted Page


class SlottedPage:
    def __init__(self):
        self.records = []

    def insert_record(self, record):
        self.records.append(record)
        print(f"Inserted {record}")

    def delete_record(self, slot):
        if 0 <= slot < len(self.records):
            if self.records[slot] is not None:
                print(f"Deleted {self.records[slot]}")
                self.records[slot] = None
            else:
                print("Slot is already empty")
        else:
            print("Invalid slot")

    def display(self):
        print("Slot Directory:", self.records)


page = SlottedPage()

page.insert_record("Alice")
page.insert_record("Bob")
page.insert_record("Charlie")

page.delete_record(1)

page.display()
