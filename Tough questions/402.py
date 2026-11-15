# Full Outer Join


students = [
    {"id": 1, "name": "Alice", "dept_id": 101},
    {"id": 2, "name": "Bob", "dept_id": 102},
    {"id": 3, "name": "Charlie", "dept_id": 103}
]

departments = [
    {"dept_id": 101, "department": "CSE"},
    {"dept_id": 102, "department": "IT"},
    {"dept_id": 104, "department": "ECE"}
]

dept_map = {
    dept["dept_id"]: dept["department"]
    for dept in departments
}

student_dept_ids = set()

print("FULL OUTER JOIN Result:")

for student in students:
    dept_id = student["dept_id"]
    student_dept_ids.add(dept_id)

    print({
        "name": student["name"],
        "department": dept_map.get(dept_id)
    })

for dept in departments:
    if dept["dept_id"] not in student_dept_ids:
        print({
            "name": None,
            "department": dept["department"]
        })
