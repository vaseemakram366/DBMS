# Sort-Merge Join Simulator


students = [
    {"id": 3, "name": "Karan"},
    {"id": 1, "name": "Aman"},
    {"id": 2, "name": "Riya"}
]

marks = [
    {"student_id": 3, "marks": 92},
    {"student_id": 1, "marks": 85},
    {"student_id": 4, "marks": 75}
]


def sort_merge_join(students, marks):
    left = sorted(students, key=lambda s: s["id"])
    right = sorted(marks, key=lambda m: m["student_id"])

    i = j = 0
    result = []

    while i < len(left) and j < len(right):
        if left[i]["id"] < right[j]["student_id"]:
            i += 1
        elif left[i]["id"] > right[j]["student_id"]:
            j += 1
        else:
            student_id = left[i]["id"]

            while i < len(left) and left[i]["id"] == student_id:
                k = j

                while k < len(right) and right[k]["student_id"] == student_id:
                    result.append({
                        "id": left[i]["id"],
                        "name": left[i]["name"],
                        "marks": right[k]["marks"]
                    })
                    k += 1

                i += 1

            while j < len(right) and right[j]["student_id"] == student_id:
                j += 1

    print("Sort-Merge Join results:")
    for row in result:
        print(row)


sort_merge_join(students, marks)
