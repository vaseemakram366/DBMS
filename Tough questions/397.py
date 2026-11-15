# Database DISTINCT Operation


records = [
    {"id": 101, "department": "CSE"},
    {"id": 102, "department": "IT"},
    {"id": 103, "department": "CSE"},
    {"id": 104, "department": "ECE"},
    {"id": 105, "department": "IT"}
]

unique_departments = set()

for record in records:
    unique_departments.add(record["department"])

print("Unique Departments:")

for department in sorted(unique_departments):
    print(department)
