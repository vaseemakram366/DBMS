# Horizontal Partitioning Simulator


class HorizontalPartition:
    def __init__(self):
        self.partition1 = []
        self.partition2 = []

    def insert(self, student):
        student_id = student["id"]

        if student_id <= 3:
            self.partition1.append(student)
            print(f"Student {student_id} added to Partition 1")
        else:
            self.partition2.append(student)
            print(f"Student {student_id} added to Partition 2")

    def show_partitions(self):
        print("Partition 1:", self.partition1)
        print("Partition 2:", self.partition2)


db = HorizontalPartition()

students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Emma"},
    {"id": 6, "name": "Frank"}
]

for student in students:
    db.insert(student)

db.show_partitions()
