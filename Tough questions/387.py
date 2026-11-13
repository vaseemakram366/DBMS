# Record Serialization and Deserialization


import json

record = {
    "id": 101,
    "name": "Alice",
    "course": "CSE"
}

# Serialization
serialized_data = json.dumps(record)

print("Serialized Data:", serialized_data)

# Deserialization
restored_record = json.loads(serialized_data)

print("Deserialized Data:", restored_record)
print("Student Name:", restored_record["name"])
