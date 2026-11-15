# Self Join Implementation


employees = [
    {"id": 1, "name": "John", "manager_id": None},
    {"id": 2, "name": "Alice", "manager_id": 1},
    {"id": 3, "name": "Bob", "manager_id": 1},
    {"id": 4, "name": "David", "manager_id": 2}
]

employee_map = {
    employee["id"]: employee["name"]
    for employee in employees
}

print("SELF JOIN Result:")

for employee in employees:
    manager_id = employee["manager_id"]

    if manager_id in employee_map:
        print({
            "employee": employee["name"],
            "manager": employee_map[manager_id]
        })
