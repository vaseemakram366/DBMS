# Inner Join Implementation


students = [
    {"id": 1, "name": "Alice", "dept_id": 101},
    {"id": 2, "name": "Bob", "dept_id": 102},
    {"id": 3, "name": "Charlie", "dept_id": 103}
]

departments = [
    {"dept_id": 101, "department": "CSE"},
    {"dept_id": 102, "department": "IT"}
]

dept_map = {
    dept["dept_id"]: dept["department"]
    for dept in departments
}

print("INNER JOIN Result:")

for student in students:
    dept_id = student["dept_id"]

    if dept_id in dept_map:
        print({
            "id": student["id"],
            "name": student["name"],
            "department": dept_map[dept_id]
        })
