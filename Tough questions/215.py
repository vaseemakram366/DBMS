# Composite Database Index Simulator


class CompositeIndex:
    def __init__(self):
        self.records = {}

    def insert(self, department, student_id, name):
        key = (department, student_id)
        self.records[key] = name
        print(f"Inserted {key}: {name}")

    def search(self, department, student_id):
        key = (department, student_id)

        if key in self.records:
            print(f"Found {key}: {self.records[key]}")
            return self.records[key]

        print(f"Record {key} not found")
        return None

    def search_department(self, department):
        results = [
            (key, name)
            for key, name in sorted(self.records.items())
            if key[0] == department
        ]

        print(f"Department {department}: {results}")
        return results


index = CompositeIndex()

index.insert("CSE", 101, "Aman")
index.insert("ECE", 102, "Riya")
index.insert("CSE", 103, "Karan")
index.insert("CSE", 104, "Neha")

index.search("CSE", 103)
index.search("ECE", 103)
index.search_department("CSE")
