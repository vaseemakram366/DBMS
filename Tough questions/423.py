# SQL Query Execution Simulation


students = [
    {"name": "Alice", "department": "CSE", "marks": 85},
    {"name": "Bob", "department": "IT", "marks": 75},
    {"name": "Charlie", "department": "CSE", "marks": 95},
    {"name": "David", "department": "CSE", "marks": 70},
    {"name": "Emma", "department": "IT", "marks": 90}
]

filtered = [
    student for student in students
    if student["department"] == "CSE"
]

sorted_students = sorted(
    filtered,
    key=lambda student: student["marks"],
    reverse=True
)

result = sorted_students[:2]

print("SQL QUERY RESULT:")

for student in result:
    print(student)
