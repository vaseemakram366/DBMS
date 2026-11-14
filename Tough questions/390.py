# Database Record Deletion


records = [
    {"id": 101, "name": "Alice"},
    {"id": 102, "name": "Bob"},
    {"id": 103, "name": "Charlie"}
]

def delete_record(record_id):
    for record in records:
        if record["id"] == record_id:
            records.remove(record)
            print("Record deleted successfully")
            return

    print("Record not found")


delete_record(102)

print("Remaining Records:")

for record in records:
    print(record)
