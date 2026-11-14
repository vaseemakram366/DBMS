# Database Record Searching


records = [
    {"id": 101, "name": "Alice", "marks": 85},
    {"id": 102, "name": "Bob", "marks": 90},
    {"id": 103, "name": "Charlie", "marks": 78}
]

def search_record(record_id):
    for record in records:
        if record["id"] == record_id:
            print("Record Found:")
            print(record)
            return

    print("Record not found")


search_record(102)
search_record(105)
