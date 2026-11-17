# ORDER BY Descending


students = [
    {"name": "Alice", "marks": 85},
    {"name": "Bob", "marks": 65},
    {"name": "Charlie", "marks": 90},
    {"name": "David", "marks": 55}
]

sorted_students = sorted(
    students,
    key=lambda student: student["marks"],
    reverse=True
)

print("ORDER BY DESC Result:")

for student in sorted_students:
    print(student)
