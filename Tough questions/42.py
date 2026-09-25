# Distributed Hash Join

from collections import defaultdict


class WorkerNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.left = []
        self.right = []

    def build_hash_table(self, key_index):
        table = defaultdict(list)

        for row in self.left:
            table[row[key_index]].append(row)

        return table

    def local_join(self, left_key, right_key):
        hash_table = defaultdict(list)

        for row in self.left:
            hash_table[row[left_key]].append(row)

        result = []

        for row in self.right:
            key = row[right_key]

            for left_row in hash_table.get(key, []):
                result.append(left_row + row)

        return result


class DistributedHashJoin:
    def __init__(self, nodes):
        self.nodes = [
            WorkerNode(i)
            for i in range(nodes)
        ]

    def partition(self, table, key_index, side):
        for row in table:
            key = row[key_index]
            node_id = hash(key) % len(self.nodes)

            if side == "left":
                self.nodes[node_id].left.append(row)
            else:
                self.nodes[node_id].right.append(row)

    def execute(
        self,
        left_table,
        right_table,
        left_key,
        right_key
    ):
        self.partition(
            left_table,
            left_key,
            "left"
        )

        self.partition(
            right_table,
            right_key,
            "right"
        )

        result = []

        for node in self.nodes:
            local_result = node.local_join(
                left_key,
                right_key
            )

            result.extend(local_result)

        return result

    def show_partitions(self):
        for node in self.nodes:
            print(f"\nWorker {node.node_id}")
            print("Left :", node.left)
            print("Right:", node.right)


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

joiner = DistributedHashJoin(3)

result = joiner.execute(
    employees,
    departments,
    2,
    0
)

joiner.show_partitions()

print("\nDistributed Join Result:")

for row in result:
    print(row)