# Grace Hash Join

class GraceHashJoin:
    def __init__(self, num_partitions=4):
        self.num_partitions = num_partitions

    def hash_function(self, key):
        return hash(key) % self.num_partitions

    def partition(self, table, key_index):
        partitions = [[] for _ in range(self.num_partitions)]

        for row in table:
            key = row[key_index]
            partition_id = self.hash_function(key)
            partitions[partition_id].append(row)

        return partitions

    def join(self, table1, table2, key1_index, key2_index):
        partitions1 = self.partition(table1, key1_index)
        partitions2 = self.partition(table2, key2_index)

        result = []

        for i in range(self.num_partitions):
            left_partition = partitions1[i]
            right_partition = partitions2[i]

            if len(left_partition) > len(right_partition):
                build = right_partition
                probe = left_partition
                build_index = key2_index
                probe_index = key1_index
                swap = True
            else:
                build = left_partition
                probe = right_partition
                build_index = key1_index
                probe_index = key2_index
                swap = False

            hash_table = {}

            for row in build:
                key = row[build_index]
                hash_table.setdefault(key, []).append(row)

            for row in probe:
                key = row[probe_index]

                if key in hash_table:
                    for matching_row in hash_table[key]:
                        if swap:
                            result.append(matching_row + row)
                        else:
                            result.append(row + matching_row)

        return result


employees = [
    (1, "Amit", 10),
    (2, "Rahul", 20),
    (3, "Vaseem", 10),
    (4, "Neha", 30),
    (5, "Arjun", 20)
]

departments = [
    (10, "CSE"),
    (20, "ECE"),
    (30, "ME")
]

joiner = GraceHashJoin(num_partitions=3)

result = joiner.join(
    employees,
    departments,
    2,
    0
)

for row in result:
    print(row)