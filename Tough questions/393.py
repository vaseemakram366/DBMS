# Database Record Filtering


records = [
    {"id": 101, "name": "Alice", "marks": 85},
    {"id": 102, "name": "Bob", "marks": 90},
    {"id": 103, "name": "Charlie", "marks": 78},
    {"id": 104, "name": "David", "marks": 65}
]

filtered_records = [
    record for record in records
    if record["marks"] >= 80
]

print("Filtered Records:")

for record in filtered_records:
    print(record)
