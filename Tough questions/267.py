# Distributed Aggregation


class DistributedAggregation:
    def __init__(self):
        self.shards = {
            "Server A": [80, 90],
            "Server B": [70, 100],
            "Server C": [60, 80]
        }

    def aggregate(self):
        total_sum = 0
        total_count = 0

        for server, marks in self.shards.items():
            local_sum = sum(marks)
            local_count = len(marks)

            total_sum += local_sum
            total_count += local_count

            print(
                f"{server} local sum: {local_sum}, "
                f"count: {local_count}"
            )

        average = total_sum / total_count if total_count else 0

        print("Global sum:", total_sum)
        print("Global count:", total_count)
        print("Global average:", average)


db = DistributedAggregation()
db.aggregate()
