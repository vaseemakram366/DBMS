# Cross Join Implementation


students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"}
]

courses = [
    {"course_id": 101, "course": "Python"},
    {"course_id": 102, "course": "DBMS"}
]

print("CROSS JOIN Result:")

for student in students:
    for course in courses:
        print({
            "name": student["name"],
            "course": course["course"]
        })
