# Approximate Query Processing using Sampling
import random
import math


class ApproximateQueryEngine:
    def __init__(self, data):
        self.data = data

    def sample(self, sample_size):
        sample_size = min(sample_size, len(self.data))
        return random.sample(self.data, sample_size)

    def approximate_avg(self, column, sample_size):
        sample = self.sample(sample_size)

        values = [row[column] for row in sample]

        average = sum(values) / len(values)

        error = self._estimate_error(values)

        return average, error

    def approximate_sum(self, column, sample_size):
        sample = self.sample(sample_size)

        values = [row[column] for row in sample]

        sample_avg = sum(values) / len(values)

        estimated_sum = sample_avg * len(self.data)

        error = self._estimate_error(values)

        return estimated_sum, error

    def _estimate_error(self, values):
        n = len(values)

        if n <= 1:
            return 0

        mean = sum(values) / n

        variance = sum(
            (x - mean) ** 2
            for x in values
        ) / (n - 1)

        standard_error = math.sqrt(variance / n)

        return standard_error


employees = [
    {"id": 1, "salary": 30000},
    {"id": 2, "salary": 45000},
    {"id": 3, "salary": 50000},
    {"id": 4, "salary": 60000},
    {"id": 5, "salary": 70000},
    {"id": 6, "salary": 80000},
    {"id": 7, "salary": 90000},
    {"id": 8, "salary": 100000},
    {"id": 9, "salary": 55000},
    {"id": 10, "salary": 65000}
]

engine = ApproximateQueryEngine(employees)

avg, error = engine.approximate_avg(
    "salary",
    sample_size=5
)

print("Approximate average:", avg)
print("Estimated standard error:", error)

total, error = engine.approximate_sum(
    "salary",
    sample_size=5
)

print("Approximate total salary:", total)