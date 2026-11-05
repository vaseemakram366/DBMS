# Distributed Query Execution


class DistributedDatabase:
    def __init__(self):
        self.shards = {
            "Server A": [
                {"id": 1, "marks": 85},
                {"id": 2, "marks": 45}
            ],
            "Server B": [
                {"id": 3, "marks": 90},
                {"id": 4, "marks": 60}
            ],
            "Server C": [
                {"id": 5, "marks": 95},
                {"id": 6, "marks": 30}
            ]
        }

    def execute_query(self, minimum_marks):
        results = []

        for server, records in self.shards.items():
            print(f"Executing query on {server}")

            for record in records:
                if record["marks"] >= minimum_marks:
                    results.append(record)

        print("Combined query result:", results)


db = DistributedDatabase()

db.execute_query(80)
