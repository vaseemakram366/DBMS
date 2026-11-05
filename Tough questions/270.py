# Distributed Join Operation


class DistributedJoin:
    def __init__(self):
        self.employees = {
            "Server A": [
                {"id": 1, "name": "Aman", "dept_id": 101},
                {"id": 2, "name": "Riya", "dept_id": 102}
            ],
            "Server B": [
                {"id": 3, "name": "Rahul", "dept_id": 101}
            ]
        }

        self.departments = {
            101: "CSE",
            102: "IT"
        }

    def execute_join(self):
        result = []

        for server, records in self.employees.items():
            for employee in records:
                dept_id = employee["dept_id"]

                if dept_id in self.departments:
                    result.append({
                        "id": employee["id"],
                        "name": employee["name"],
                        "department": self.departments[dept_id]
                    })

        print("Distributed Join Result:")

        for record in result:
            print(record)


db = DistributedJoin()
db.execute_join()
