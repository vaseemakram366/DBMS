# Row-Level Security (RLS) Policy Engine


class RowLevelSecurity:
    def __init__(self):
        self.users = {}
        self.records = []

    def add_user(self, username, role, employee_id=None):
        self.users[username] = {
            "role": role,
            "employee_id": employee_id
        }

    def insert_record(self, employee_id, name, salary, department):
        self.records.append({
            "employee_id": employee_id,
            "name": name,
            "salary": salary,
            "department": department
        })

    def can_access(self, username, record):
        user = self.users.get(username)

        if user is None:
            return False

        if user["role"] == "admin":
            return True

        if user["role"] == "hr":
            return True

        if user["role"] == "employee":
            return user["employee_id"] == record["employee_id"]

        return False

    def select_records(self, username):
        if username not in self.users:
            raise PermissionError("Unknown user")

        return [
            record.copy()
            for record in self.records
            if self.can_access(username, record)
        ]

    def update_salary(self, username, employee_id, new_salary):
        if username not in self.users:
            raise PermissionError("Unknown user")

        for record in self.records:
            if record["employee_id"] == employee_id:
                if not self.can_access(username, record):
                    raise PermissionError("Access denied")

                if self.users[username]["role"] not in ("admin", "hr"):
                    raise PermissionError("Salary update not allowed")

                record["salary"] = new_salary
                return "Salary updated successfully"

        return "Record not found"


db = RowLevelSecurity()

db.add_user("admin1", "admin")
db.add_user("hr1", "hr")
db.add_user("employee1", "employee", 101)
db.add_user("employee2", "employee", 102)

db.insert_record(101, "Aman", 30000, "IT")
db.insert_record(102, "Riya", 40000, "HR")
db.insert_record(103, "Rahul", 35000, "IT")

print("Employee 101:")
print(db.select_records("employee1"))

print("\nHR access:")
print(db.select_records("hr1"))

print("\nAdmin access:")
print(db.select_records("admin1"))

print("\nSalary update:")
print(db.update_salary("hr1", 101, 50000))
