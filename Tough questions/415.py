# MIN Aggregate Function


students = [
    {"name": "Alice", "marks": 85},
    {"name": "Bob", "marks": 65},
    {"name": "Charlie", "marks": 90},
    {"name": "David", "marks": 55}
]

minimum_marks = min(
    student["marks"] for student in students
)

print("MIN Result:")
print("Minimum Marks:", minimum_marks)
