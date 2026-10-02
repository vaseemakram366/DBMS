# Equi-Depth Histogram Cardinality Estimator

from bisect import bisect_right


class EquiDepthHistogram:
    def __init__(self, values, bucket_count):
        if not values:
            raise ValueError("Values cannot be empty")

        self.values = sorted(values)
        self.bucket_count = min(
            bucket_count,
            len(values)
        )

        self.buckets = []
        self.build()

    def build(self):
        n = len(self.values)

        for i in range(self.bucket_count):
            start = (i * n) // self.bucket_count
            end = ((i + 1) * n) // self.bucket_count

            bucket_values = self.values[start:end]

            self.buckets.append({
                "min": bucket_values[0],
                "max": bucket_values[-1],
                "count": len(bucket_values)
            })

    def estimate_less_than(self, value):
        total = 0

        for bucket in self.buckets:
            low = bucket["min"]
            high = bucket["max"]
            count = bucket["count"]

            if value > high:
                total += count

            elif value <= low:
                break

            else:
                fraction = (
                    (value - low) /
                    (high - low)
                    if high != low
                    else 0
                )

                total += fraction * count
                break

        return total

    def estimate_greater_than(self, value):
        return len(self.values) - self.estimate_less_than(value)

    def estimate_equal(self, value):
        for bucket in self.buckets:
            if bucket["min"] <= value <= bucket["max"]:
                return bucket["count"] / max(
                    1,
                    bucket["max"] - bucket["min"] + 1
                )

        return 0

    def show(self):
        print("\nEqui-Depth Histogram")
        print("-" * 45)

        for i, bucket in enumerate(self.buckets):
            print(
                f"Bucket {i + 1}: "
                f"[{bucket['min']}, {bucket['max']}] "
                f"Rows={bucket['count']}"
            )


class QueryOptimizer:
    def __init__(self, values):
        self.values = values
        self.histogram = EquiDepthHistogram(
            values,
            bucket_count=5
        )

    def estimate_selectivity(self, operator, value):
        total_rows = len(self.values)

        if operator == "<":
            estimated = (
                self.histogram.estimate_less_than(value)
            )

        elif operator == ">":
            estimated = (
                self.histogram.estimate_greater_than(value)
            )

        elif operator == "=":
            estimated = (
                self.histogram.estimate_equal(value)
            )

        else:
            raise ValueError(
                "Unsupported operator"
            )

        return estimated / total_rows

    def estimate_rows(self, operator, value):
        selectivity = self.estimate_selectivity(
            operator,
            value
        )

        return selectivity * len(self.values)


if __name__ == "__main__":
    salaries = [
        25000, 27000, 30000, 32000,
        35000, 38000, 40000, 42000,
        45000, 47000, 50000, 52000,
        55000, 58000, 60000, 63000,
        65000, 68000, 70000, 75000,
        80000, 85000, 90000, 95000,
        100000
    ]

    optimizer = QueryOptimizer(salaries)

    optimizer.histogram.show()

    print("\nEstimated rows:")
    print(
        "salary < 60000:",
        optimizer.estimate_rows("<", 60000)
    )

    print(
        "salary > 70000:",
        optimizer.estimate_rows(">", 70000)
    )

    print(
        "salary = 50000:",
        optimizer.estimate_rows("=", 50000)
    )