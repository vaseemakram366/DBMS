# Hash Join Simulator


students = [
    {"id": 1, "name": "Aman"},
    {"id": 2, "name": "Riya"},
    {"id": 3, "name": "Karan"}
]

marks = [
    {"student_id": 1, "marks": 85},
    {"student_id": 3, "marks": 92},
    {"student_id": 4, "marks": 75}
]


def hash_join(students, marks):
    hash_table = {}

    for mark in marks:
        key = mark["student_id"]
        hash_table.setdefault(key, []).append(mark)

    result = []
    probes = 0

    for student in students:
        probes += 1

        matching_marks = hash_table.get(student["id"], [])

        for mark in matching_marks:
            result.append({
                "id": student["id"],
                "name": student["name"],
                "marks": mark["marks"]
            })

    print("Hash Join results:")
    for row in result:
        print(row)

    print("Hash probes:", probes)


hash_join(students, marks)
