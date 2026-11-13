# Fixed-Length Record Storage


class FixedRecordStorage:
    def __init__(self, size):
        self.size = size
        self.records = []

    def insert_record(self, name):
        if len(name) > self.size:
            print(f"{name} is too long")
            return

        record = name.ljust(self.size)
        self.records.append(record)

        print(f"Inserted: '{record}'")

    def display(self):
        print("\nStored Records:")
        for record in self.records:
            print(record)


storage = FixedRecordStorage(10)

storage.insert_record("Alice")
storage.insert_record("Ram")
storage.insert_record("Christopher")

storage.display()
