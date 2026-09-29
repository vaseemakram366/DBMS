# Partition Pruning Engine

class Partition:
    def __init__(self, name, min_value, max_value):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.rows = []

    def contains(self, value):
        return self.min_value <= value < self.max_value

    def insert(self, row):
        if self.contains(row["id"]):
            self.rows.append(row)
            return True
        return False


class PartitionedTable:
    def __init__(self):
        self.partitions = []

    def add_partition(self, name, min_value, max_value):
        self.partitions.append(
            Partition(name, min_value, max_value)
        )

    def insert(self, row):
        for partition in self.partitions:
            if partition.insert(row):
                return

        raise ValueError("No partition found for row")

    def prune_partitions(self, query_min, query_max):
        selected = []

        for partition in self.partitions:
            if (
                partition.max_value > query_min
                and partition.min_value < query_max
            ):
                selected.append(partition)

        return selected

    def range_query(self, query_min, query_max):
        partitions = self.prune_partitions(
            query_min,
            query_max
        )

        result = []

        for partition in partitions:
            for row in partition.rows:
                if query_min <= row["id"] < query_max:
                    result.append(row)

        return partitions, result

    def show_partitions(self):
        for partition in self.partitions:
            print(
                partition.name,
                f"[{partition.min_value}, {partition.max_value})",
                "Rows:",
                len(partition.rows)
            )


if __name__ == "__main__":
    table = PartitionedTable()

    table.add_partition("P1", 0, 100)
    table.add_partition("P2", 100, 200)
    table.add_partition("P3", 200, 300)
    table.add_partition("P4", 300, 400)

    for i in range(0, 400, 25):
        table.insert({
            "id": i,
            "name": f"User{i}"
        })

    print("All Partitions:")
    table.show_partitions()

    print("\nQuery: id >= 125 AND id < 225")

    partitions, result = table.range_query(125, 225)

    print("\nPartitions Scanned:")

    for partition in partitions:
        print(partition.name)

    print("\nQuery Result:")

    for row in result:
        print(row)