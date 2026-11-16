# Group By Implementation


employees = [
    {"name": "Alice", "department": "CSE"},
    {"name": "Bob", "department": "IT"},
    {"name": "Charlie", "department": "CSE"},
    {"name": "David", "department": "IT"},
    {"name": "Emma", "department": "ECE"}
]

department_count = {}

for employee in employees:
    dept = employee["department"]

    if dept not in department_count:
        department_count[dept] = 0

    department_count[dept] += 1

print("GROUP BY Result:")

for dept, count in department_count.items():
    print(dept, ":", count)
