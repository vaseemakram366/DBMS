# SQL Query Execution Plan Simulator


class QueryPlanSimulator:
    def __init__(self, table_name, rows):
        self.table_name = table_name
        self.rows = rows

    def execute(self, minimum_marks):
        print("Execution Plan:")
        print(f"1. Table Scan: {self.table_name}")
        print(f"2. Filter: marks >= {minimum_marks}")
        print("3. Return Results")

        result = [
            row for row in self.rows
            if row["marks"] >= minimum_marks
        ]

        print("\nQuery Results:")
        for row in result:
            print(row)

        return result


students = [
    {"id": 101, "name": "Aman", "marks": 85},
    {"id": 102, "name": "Riya", "marks": 92},
    {"id": 103, "name": "Karan", "marks": 70},
    {"id": 104, "name": "Neha", "marks": 88}
]

query = QueryPlanSimulator("Students", students)
query.execute(85)
