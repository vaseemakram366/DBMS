# Merkle Tree Replica Synchronization

import hashlib


class MerkleNode:
    def __init__(self, hash_value, left=None, right=None):
        self.hash = hash_value
        self.left = left
        self.right = right


class MerkleTree:
    def __init__(self, data):
        self.data = sorted(data)
        self.root = self.build_tree(self.data)

    def hash_data(self, value):
        return hashlib.sha256(
            str(value).encode()
        ).hexdigest()

    def hash_pair(self, left, right):
        return hashlib.sha256(
            (left + right).encode()
        ).hexdigest()

    def build_tree(self, data):
        if not data:
            return None

        nodes = [
            MerkleNode(self.hash_data(value))
            for value in data
        ]

        while len(nodes) > 1:
            next_level = []

            for i in range(0, len(nodes), 2):
                left = nodes[i]
                right = nodes[i + 1] if i + 1 < len(nodes) else left

                parent_hash = self.hash_pair(
                    left.hash,
                    right.hash
                )

                next_level.append(
                    MerkleNode(
                        parent_hash,
                        left,
                        right
                    )
                )

            nodes = next_level

        return nodes[0]

    def root_hash(self):
        return self.root.hash if self.root else None


class ReplicaSynchronizer:
    def __init__(self, replica_a, replica_b):
        self.replica_a = sorted(replica_a)
        self.replica_b = sorted(replica_b)

        self.tree_a = MerkleTree(self.replica_a)
        self.tree_b = MerkleTree(self.replica_b)

    def compare(self):
        if self.tree_a.root_hash() == self.tree_b.root_hash():
            return []

        differences = []

        all_keys = set(self.replica_a) | set(self.replica_b)

        for key in sorted(all_keys):
            if key not in self.replica_a:
                differences.append(
                    ("MISSING_IN_A", key)
                )
            elif key not in self.replica_b:
                differences.append(
                    ("MISSING_IN_B", key)
                )

        return differences

    def synchronize(self):
        self.replica_a = sorted(
            set(self.replica_a) | set(self.replica_b)
        )

        self.replica_b = sorted(
            set(self.replica_a) | set(self.replica_b)
        )

        self.tree_a = MerkleTree(self.replica_a)
        self.tree_b = MerkleTree(self.replica_b)


if __name__ == "__main__":
    replica_a = [
        "user:1",
        "user:2",
        "user:3",
        "user:4",
        "user:5"
    ]

    replica_b = [
        "user:1",
        "user:2",
        "user:3",
        "user:6",
        "user:5"
    ]

    sync = ReplicaSynchronizer(
        replica_a,
        replica_b
    )

    print("Replica A Root:")
    print(sync.tree_a.root_hash())

    print("\nReplica B Root:")
    print(sync.tree_b.root_hash())

    differences = sync.compare()

    print("\nDifferences:")

    for difference in differences:
        print(difference)

    sync.synchronize()

    print("\nAfter Synchronization:")
    print(
        sync.tree_a.root_hash()
        == sync.tree_b.root_hash()
    )