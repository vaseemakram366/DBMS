# SUM Aggregate Function


employees = [
    {"name": "Alice", "salary": 30000},
    {"name": "Bob", "salary": 40000},
    {"name": "Charlie", "salary": 35000},
    {"name": "David", "salary": 50000}
]

total_salary = sum(
    employee["salary"] for employee in employees
)

print("SUM Result:")
print("Total Salary:", total_salary)
