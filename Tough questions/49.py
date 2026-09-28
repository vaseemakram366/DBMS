# External Hash Aggregation

from collections import defaultdict
import os
import tempfile


class ExternalHashAggregation:
    def __init__(self, memory_limit=3, partitions=4):
        self.memory_limit = memory_limit
        self.partitions = partitions

    def _hash_partition(self, key):
        return hash(key) % self.partitions

    def partition_data(self, rows):
        files = []

        for i in range(self.partitions):
            file = tempfile.NamedTemporaryFile(
                mode="w+",
                delete=False
            )
            files.append(file)

        for row in rows:
            partition = self._hash_partition(row["department"])
            files[partition].write(
                f'{row["department"]},{row["salary"]}\n'
            )

        for file in files:
            file.close()

        return [file.name for file in files]

    def aggregate_partition(self, filename):
        result = defaultdict(lambda: [0, 0])

        with open(filename, "r") as file:
            for line in file:
                department, salary = line.strip().split(",")

                salary = int(salary)

                result[department][0] += 1
                result[department][1] += salary

        return result

    def execute(self, rows):
        partition_files = self.partition_data(rows)
        final_result = defaultdict(lambda: [0, 0])

        try:
            for filename in partition_files:
                partial_result = self.aggregate_partition(filename)

                for department, values in partial_result.items():
                    final_result[department][0] += values[0]
                    final_result[department][1] += values[1]

        finally:
            for filename in partition_files:
                if os.path.exists(filename):
                    os.remove(filename)

        return final_result


if __name__ == "__main__":
    employees = [
        {"name": "Aman", "department": "IT", "salary": 50000},
        {"name": "Rahul", "department": "HR", "salary": 45000},
        {"name": "Priya", "department": "IT", "salary": 60000},
        {"name": "Neha", "department": "Sales", "salary": 40000},
        {"name": "Riya", "department": "HR", "salary": 55000},
        {"name": "Karan", "department": "IT", "salary": 70000},
        {"name": "Arjun", "department": "Sales", "salary": 50000},
        {"name": "Simran", "department": "HR", "salary": 65000}
    ]

    engine = ExternalHashAggregation(
        memory_limit=3,
        partitions=4
    )

    result = engine.execute(employees)

    print("Department-wise Aggregation")
    print("-" * 45)

    for department, values in sorted(result.items()):
        count, total_salary = values
        average = total_salary / count

        print(
            f"{department:<10} "
            f"Count = {count:<3} "
            f"Total = {total_salary:<7} "
            f"Average = {average:.2f}"
        )