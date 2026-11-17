# AVG Aggregate Function


students = [
    {"name": "Alice", "marks": 80},
    {"name": "Bob", "marks": 70},
    {"name": "Charlie", "marks": 90},
    {"name": "David", "marks": 60}
]

total_marks = sum(
    student["marks"] for student in students
)

average = total_marks / len(students)

print("AVG Result:")
print("Average Marks:", average)
