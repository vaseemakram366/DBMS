# Table Scan vs Index Scan Simulator


class ScanComparison:
    def __init__(self, records):
        self.records = records

        # Build a hash-based index on student ID.
        self.index = {
            record["id"]: record
            for record in records
        }

    def table_scan(self, student_id):
        checks = 0

        for record in self.records:
            checks += 1

            if record["id"] == student_id:
                print("Table Scan result:", record)
                print("Table Scan records checked:", checks)
                return record

        print("Student not found")
        print("Table Scan records checked:", checks)
        return None

    def index_scan(self, student_id):
        print("Index Scan result:", self.index.get(student_id))
        print("Index lookups: 1")
        return self.index.get(student_id)


students = [
    {"id": 101, "name": "Aman"},
    {"id": 102, "name": "Riya"},
    {"id": 103, "name": "Karan"},
    {"id": 104, "name": "Neha"},
    {"id": 105, "name": "Vikas"}
]

db = ScanComparison(students)

print("--- Table Scan ---")
db.table_scan(103)

print("\n--- Index Scan ---")
db.index_scan(103)
