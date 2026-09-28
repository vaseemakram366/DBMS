class MaterializedView:
    def __init__(self):
        self.groups = {}

    def _add(self, dept, salary):
        if dept not in self.groups:
            self.groups[dept] = {"count": 0, "sum": 0}

        self.groups[dept]["count"] += 1
        self.groups[dept]["sum"] += salary

    def _remove(self, dept, salary):
        if dept not in self.groups:
            return

        self.groups[dept]["count"] -= 1
        self.groups[dept]["sum"] -= salary

        if self.groups[dept]["count"] == 0:
            del self.groups[dept]

    def insert(self, employee):
        self._add(employee["dept"], employee["salary"])

    def delete(self, employee):
        self._remove(employee["dept"], employee["salary"])

    def update(self, old_employee, new_employee):
        self.delete(old_employee)
        self.insert(new_employee)

    def display(self):
        for dept, values in sorted(self.groups.items()):
            count = values["count"]
            total = values["sum"]
            average = total / count if count else 0

            print({
                "department": dept,
                "count": count,
                "total_salary": total,
                "average_salary": round(average, 2)
            })


employees = [
    {"id": 1, "dept": "IT", "salary": 60000},
    {"id": 2, "dept": "HR", "salary": 40000},
    {"id": 3, "dept": "IT", "salary": 80000}
]

view = MaterializedView()

for employee in employees:
    view.insert(employee)

print("Initial Materialized View:")
view.display()

old_employee = employees[0]
new_employee = {"id": 1, "dept": "HR", "salary": 70000}

view.update(old_employee, new_employee)

print("\nAfter Employee Update:")
view.display()

view.delete(employees[1])

print("\nAfter Employee Deletion:")
view.display()