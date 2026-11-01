# Database Indexing Simulator


class DatabaseIndex:
    def __init__(self):
        self.records = {}
        self.index = {}

    def insert(self, student_id, name, marks):
        record = {
            "id": student_id,
            "name": name,
            "marks": marks
        }

        self.records[student_id] = record
        self.index[student_id] = student_id

        print(f"Inserted student {student_id}")

    def search(self, student_id):
        if student_id not in self.index:
            print(f"Student {student_id} not found")
            return None

        record_id = self.index[student_id]
        record = self.records[record_id]

        print("Found:", record)
        return record

    def show_index(self):
        print("Index:", self.index)


db = DatabaseIndex()

db.insert(101, "Aman", 85)
db.insert(102, "Riya", 92)
db.insert(103, "Karan", 78)

db.show_index()
db.search(102)
db.search(105)
