# Vertical Database Partitioning


class VerticalPartition:
    def __init__(self):
        self.basic_info = {}
        self.academic_info = {}

    def insert_student(self, student_id, name, email, marks):
        self.basic_info[student_id] = {
            "name": name
        }

        self.academic_info[student_id] = {
            "email": email,
            "marks": marks
        }

        print(f"Student {student_id} inserted")

    def show_partitions(self):
        print("Basic Information:", self.basic_info)
        print("Academic Information:", self.academic_info)

    def get_student(self, student_id):
        if student_id not in self.basic_info:
            print("Student not found")
            return

        student = {
            "id": student_id,
            **self.basic_info[student_id],
            **self.academic_info[student_id]
        }

        print("Complete Student:", student)


db = VerticalPartition()

db.insert_student(1, "Alice", "alice@gmail.com", 90)
db.insert_student(2, "Bob", "bob@gmail.com", 85)

db.show_partitions()
db.get_student(1)
