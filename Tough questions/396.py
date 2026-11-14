# Database Grouping Simulation


from collections import defaultdict

records = [
    {"name": "Alice", "department": "CSE"},
    {"name": "Bob", "department": "IT"},
    {"name": "Charlie", "department": "CSE"},
    {"name": "David", "department": "IT"},
    {"name": "Eve", "department": "ECE"}
]

groups = defaultdict(list)

for record in records:
    department = record["department"]
    groups[department].append(record["name"])

for department, students in groups.items():
    print(department, ":", students)
