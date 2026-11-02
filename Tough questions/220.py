# Nested Loop Join Simulator


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


def nested_loop_join(students, marks):
    result = []
    comparisons = 0

    for student in students:
        for mark in marks:
            comparisons += 1

            if student["id"] == mark["student_id"]:
                result.append({
                    "id": student["id"],
                    "name": student["name"],
                    "marks": mark["marks"]
                })

    print("Nested Loop Join results:")
    for row in result:
        print(row)

    print("Total comparisons:", comparisons)


nested_loop_join(students, marks)
