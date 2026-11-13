# Variable-Length Record Storage


class VariableRecordStorage:
    def __init__(self):
        self.records = []

    def insert_record(self, name):
        self.records.append(name)
        print(f"Inserted: {name}, Length: {len(name)}")

    def display(self):
        print("\nStored Records:")
        for record in self.records:
            print(record)


storage = VariableRecordStorage()

storage.insert_record("Alice")
storage.insert_record("Christopher")
storage.insert_record("Ram")

storage.display()
