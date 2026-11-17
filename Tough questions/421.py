# OFFSET Clause Simulation


students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Emma"}
]

offset = 2

result = students[offset:]

print("OFFSET Result:")

for student in result:
    print(student)
