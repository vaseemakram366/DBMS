# Horizontal Partitioning Simulation

students = [
    {"id": 1, "name": "Aman", "marks": 85},
    {"id": 2, "name": "Rahul", "marks": 45},
    {"id": 3, "name": "Priya", "marks": 92},
    {"id": 4, "name": "Karan", "marks": 38},
    {"id": 5, "name": "Neha", "marks": 76}
]

high_marks = []
low_marks = []

# Partition rows based on marks
for student in students:
    if student["marks"] >= 60:
        high_marks.append(student)
    else:
        low_marks.append(student)

print("High Marks Partition:", high_marks)
print("Low Marks Partition:", low_marks)