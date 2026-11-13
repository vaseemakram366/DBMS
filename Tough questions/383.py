# Record Search in Slotted Page


class SlottedPage:
    def __init__(self):
        self.records = []

    def insert_record(self, record):
        self.records.append(record)

    def search_record(self, target):
        for slot, record in enumerate(self.records):
            if record == target:
                print(f"Record found at slot {slot}")
                return slot

        print("Record not found")
        return -1


page = SlottedPage()

page.insert_record("Alice")
page.insert_record("Bob")
page.insert_record("Charlie")

page.search_record("Bob")
page.search_record("David")
