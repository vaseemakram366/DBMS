# MAX Aggregate Function


students = [
    {"name": "Alice", "marks": 85},
    {"name": "Bob", "marks": 65},
    {"name": "Charlie", "marks": 90},
    {"name": "David", "marks": 55}
]

maximum_marks = max(
    student["marks"] for student in students
)

print("MAX Result:")
print("Maximum Marks:", maximum_marks)
