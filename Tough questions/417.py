# HAVING Clause Simulation


employees = [
    {"name": "Alice", "department": "CSE"},
    {"name": "Bob", "department": "IT"},
    {"name": "Charlie", "department": "CSE"},
    {"name": "David", "department": "IT"},
    {"name": "Emma", "department": "CSE"},
    {"name": "Frank", "department": "ECE"}
]

department_count = {}

for employee in employees:
    dept = employee["department"]

    department_count[dept] = department_count.get(dept, 0) + 1

print("HAVING Result:")

for dept, count in department_count.items():
    if count >= 2:
        print(dept, ":", count)
