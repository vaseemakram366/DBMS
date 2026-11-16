# Anti Join Implementation


students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"}
]

enrollments = [
    {"student_id": 1, "course": "Python"},
    {"student_id": 2, "course": "DBMS"}
]

enrolled_ids = {
    enrollment["student_id"]
    for enrollment in enrollments
}

print("ANTI JOIN Result:")

for student in students:
    if student["id"] not in enrolled_ids:
        print(student)
