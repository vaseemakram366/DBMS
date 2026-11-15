# Database Join Simulation


students = [
    {"id": 1, "name": "Alice", "dept_id": 101},
    {"id": 2, "name": "Bob", "dept_id": 102},
    {"id": 3, "name": "Charlie", "dept_id": 101}
]

departments = [
    {"dept_id": 101, "department": "CSE"},
    {"dept_id": 102, "department": "IT"}
]

print("Joined Records:")

for student in students:
    for dept in departments:
        if student["dept_id"] == dept["dept_id"]:
            print({
                "name": student["name"],
                "department": dept["department"]
            })
