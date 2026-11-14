# Database Record Sorting


records = [
    {"id": 101, "name": "Alice", "marks": 85},
    {"id": 102, "name": "Bob", "marks": 90},
    {"id": 103, "name": "Charlie", "marks": 78}
]

records.sort(key=lambda record: record["marks"])

print("Records Sorted by Marks:")

for record in records:
    print(record)
