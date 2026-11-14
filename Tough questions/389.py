# Database Record Update


records = [
    {"id": 101, "name": "Alice", "marks": 85},
    {"id": 102, "name": "Bob", "marks": 90},
    {"id": 103, "name": "Charlie", "marks": 78}
]

def update_record(record_id, new_name, new_marks):
    for record in records:
        if record["id"] == record_id:
            record["name"] = new_name
            record["marks"] = new_marks
            print("Record updated successfully")
            return

    print("Record not found")


update_record(102, "Bobby", 95)

print("Updated Database:")

for record in records:
    print(record)
