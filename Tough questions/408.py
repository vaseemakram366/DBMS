# Semi Join Implementation


students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"}
]

enrollments = [
    {"student_id": 1, "course": "Python"},
    {"student_id": 2, "course": "DBMS"}
]

enrolled_ids = {
    enrollment["student_id"]
    for enrollment in enrollments
}

print("SEMI JOIN Result:")

for student in students:
    if student["id"] in enrolled_ids:
        print(student)
