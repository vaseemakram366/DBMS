# Binary Record Storage


import pickle

records = [
    {"id": 101, "name": "Alice"},
    {"id": 102, "name": "Bob"},
    {"id": 103, "name": "Charlie"}
]

# Store records in binary file
with open("database.dat", "wb") as file:
    pickle.dump(records, file)

print("Records stored successfully")

# Read records from binary file
with open("database.dat", "rb") as file:
    loaded_records = pickle.load(file)

print("Retrieved Records:")

for record in loaded_records:
    print(record)
