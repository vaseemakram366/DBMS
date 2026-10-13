# Partition-Wise Parallel Aggregation


from concurrent.futures import ThreadPoolExecutor
from math import ceil


class ParallelAggregator:
    def __init__(self, workers=4):
        if workers <= 0:
            raise ValueError("Workers must be positive")

        self.workers = workers

    def partition_data(self, records):
        if not records:
            return []

        size = ceil(len(records) / self.workers)

        return [
            records[i:i + size]
            for i in range(0, len(records), size)
        ]

    def aggregate_partition(self, partition):
        total_salary = sum(
            record["salary"] for record in partition
        )

        count = len(partition)

        return {
            "sum": total_salary,
            "count": count,
            "min": min(
                (record["salary"] for record in partition),
                default=None
            ),
            "max": max(
                (record["salary"] for record in partition),
                default=None
            )
        }

    def aggregate(self, records):
        partitions = self.partition_data(records)

        if not partitions:
            return {
                "sum": 0,
                "count": 0,
                "avg": None,
                "min": None,
                "max": None
            }

        with ThreadPoolExecutor(
            max_workers=self.workers
        ) as executor:
            partial_results = list(
                executor.map(
                    self.aggregate_partition,
                    partitions
                )
            )

        total_sum = sum(r["sum"] for r in partial_results)
        total_count = sum(r["count"] for r in partial_results)

        return {
            "sum": total_sum,
            "count": total_count,
            "avg": total_sum / total_count,
            "min": min(r["min"] for r in partial_results),
            "max": max(r["max"] for r in partial_results)
        }


employees = [
    {"id": 1, "salary": 30000},
    {"id": 2, "salary": 45000},
    {"id": 3, "salary": 50000},
    {"id": 4, "salary": 35000},
    {"id": 5, "salary": 60000},
    {"id": 6, "salary": 40000},
    {"id": 7, "salary": 55000},
    {"id": 8, "salary": 65000}
]

aggregator = ParallelAggregator(workers=4)
result = aggregator.aggregate(employees)

print("Total salary:", result["sum"])
print("Employee count:", result["count"])
print("Average salary:", result["avg"])
print("Minimum salary:", result["min"])
print("Maximum salary:", result["max"])
