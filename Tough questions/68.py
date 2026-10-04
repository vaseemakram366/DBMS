# Predicate Pushdown Engine

class Table:
    def __init__(self, name, rows):
        self.name = name
        self.rows = rows


class QueryPlan:
    def __init__(self, tables):
        self.tables = tables

    def execute_without_pushdown(self, predicate):
        joined = []

        employees = self.tables["employees"].rows
        departments = self.tables["departments"].rows

        for emp in employees:
            for dept in departments:
                if emp["dept_id"] == dept["id"]:
                    joined.append({
                        "name": emp["name"],
                        "salary": emp["salary"],
                        "department": dept["name"]
                    })

        return [
            row for row in joined
            if predicate(row)
        ]

    def execute_with_pushdown(self, employee_predicate):
        filtered_employees = [
            emp
            for emp in self.tables["employees"].rows
            if employee_predicate(emp)
        ]

        result = []

        for emp in filtered_employees:
            for dept in self.tables["departments"].rows:
                if emp["dept_id"] == dept["id"]:
                    result.append({
                        "name": emp["name"],
                        "salary": emp["salary"],
                        "department": dept["name"]
                    })

        return result


employees = Table(
    "employees",
    [
        {"id": 1, "name": "Aman", "salary": 45000, "dept_id": 1},
        {"id": 2, "name": "Rahul", "salary": 80000, "dept_id": 2},
        {"id": 3, "name": "Priya", "salary": 70000, "dept_id": 1},
        {"id": 4, "name": "Neha", "salary": 40000, "dept_id": 3},
        {"id": 5, "name": "Ravi", "salary": 90000, "dept_id": 2}
    ]
)

departments = Table(
    "departments",
    [
        {"id": 1, "name": "CSE"},
        {"id": 2, "name": "IT"},
        {"id": 3, "name": "HR"}
    ]
)


plan = QueryPlan({
    "employees": employees,
    "departments": departments
})


predicate = lambda row: row["salary"] > 60000

result1 = plan.execute_without_pushdown(predicate)

result2 = plan.execute_with_pushdown(
    lambda row: row["salary"] > 60000
)


print("Without Predicate Pushdown:")
for row in result1:
    print(row)

print("\nWith Predicate Pushdown:")
for row in result2:
    print(row)