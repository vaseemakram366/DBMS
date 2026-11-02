# SQL Join Algorithms Simulator


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


def inner_join(students, marks):
    result = []

    for student in students:
        for mark in marks:
            if student["id"] == mark["student_id"]:
                result.append({
                    "id": student["id"],
                    "name": student["name"],
                    "marks": mark["marks"]
                })

    return result


print("INNER JOIN results:")
for row in inner_join(students, marks):
    print(row)
