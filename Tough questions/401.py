# Right Outer Join


students = [
    {"id": 1, "name": "Alice", "dept_id": 101},
    {"id": 2, "name": "Bob", "dept_id": 102}
]

departments = [
    {"dept_id": 101, "department": "CSE"},
    {"dept_id": 102, "department": "IT"},
    {"dept_id": 103, "department": "ECE"}
]

student_map = {}

for student in students:
    student_map.setdefault(student["dept_id"], []).append(student["name"])

print("RIGHT OUTER JOIN Result:")

for dept in departments:
    names = student_map.get(dept["dept_id"], [])

    if names:
        for name in names:
            print({
                "name": name,
                "department": dept["department"]
            })
    else:
        print({
            "name": None,
            "department": dept["department"]
        })
