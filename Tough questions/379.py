# Database Page Compaction


class DatabasePage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.records = []

    def insert_record(self, size):
        self.records.append(size)
        print(f"Record of size {size} inserted")

    def delete_record(self, index):
        if 0 <= index < len(self.records):
            removed = self.records.pop(index)
            print(f"Record of size {removed} deleted")

    def compact(self):
        used = sum(self.records)
        free = self.capacity - used

        print("Page compacted")
        print("Records:", self.records)
        print("Used Space:", used)
        print("Continuous Free Space:", free)


page = DatabasePage(100)

page.insert_record(20)
page.insert_record(30)
page.insert_record(25)

page.delete_record(1)

page.compact()
