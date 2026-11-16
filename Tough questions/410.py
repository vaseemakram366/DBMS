# Division Operation


enrollments = [
    {"student": "Alice", "course": "Python"},
    {"student": "Alice", "course": "DBMS"},
    {"student": "Bob", "course": "Python"},
    {"student": "Charlie", "course": "Python"},
    {"student": "Charlie", "course": "DBMS"}
]

required_courses = {"Python", "DBMS"}

students = {record["student"] for record in enrollments}

print("DIVISION Result:")

for student in students:
    completed_courses = {
        record["course"]
        for record in enrollments
        if record["student"] == student
    }

    if required_courses.issubset(completed_courses):
        print(student)
