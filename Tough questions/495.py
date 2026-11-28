# Vertical Partitioning Simulation

students = [
    {"id": 1, "name": "Aman", "email": "aman@gmail.com", "marks": 85},
    {"id": 2, "name": "Rahul", "email": "rahul@gmail.com", "marks": 90},
    {"id": 3, "name": "Priya", "email": "priya@gmail.com", "marks": 95}
]

# Vertical partition 1
personal_data = [
    {"id": s["id"], "name": s["name"]}
    for s in students
]

# Vertical partition 2
academic_data = [
    {"id": s["id"], "email": s["email"], "marks": s["marks"]}
    for s in students
]

print("Personal Data:", personal_data)
print("Academic Data:", academic_data)

# Reconstruct original table using ID
academic_map = {s["id"]: s for s in academic_data}

restored = []

for student in personal_data:
    combined = student.copy()
    combined.update(academic_map[student["id"]])
    restored.append(combined)

print("Restored Table:", restored)