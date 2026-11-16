# Theta Join Implementation


employees = [
    {"id": 1, "name": "Alice", "salary": 25000},
    {"id": 2, "name": "Bob", "salary": 40000},
    {"id": 3, "name": "Charlie", "salary": 50000}
]

salary_grades = [
    {"grade": "A", "minimum_salary": 30000},
    {"grade": "B", "minimum_salary": 45000}
]

print("THETA JOIN Result:")

for employee in employees:
    for grade in salary_grades:
        if employee["salary"] > grade["minimum_salary"]:
            print({
                "name": employee["name"],
                "salary": employee["salary"],
                "grade": grade["grade"]
            })
