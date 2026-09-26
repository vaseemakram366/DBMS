# Consistent Hashing for Distributed Database Nodes

import hashlib
import bisect


class ConsistentHashRing:
    def __init__(self, virtual_nodes=3):
        self.virtual_nodes = virtual_nodes
        self.ring = {}
        self.positions = []

    def hash_key(self, key):
        digest = hashlib.sha256(
            str(key).encode()
        ).hexdigest()

        return int(digest, 16)

    def add_node(self, node):
        for i in range(self.virtual_nodes):
            virtual_key = f"{node}#{i}"
            position = self.hash_key(virtual_key)

            self.ring[position] = node
            self.positions.append(position)

        self.positions.sort()

    def remove_node(self, node):
        positions_to_remove = [
            position
            for position, owner in self.ring.items()
            if owner == node
        ]

        for position in positions_to_remove:
            del self.ring[position]
            self.positions.remove(position)

    def get_node(self, key):
        if not self.positions:
            return None

        position = self.hash_key(key)

        index = bisect.bisect_left(
            self.positions,
            position
        )

        if index == len(self.positions):
            index = 0

        return self.ring[self.positions[index]]

    def show_ring(self):
        print("\nHash Ring:")

        for position in self.positions:
            print(
                position,
                "->",
                self.ring[position]
            )


ring = ConsistentHashRing(
    virtual_nodes=5
)

ring.add_node("DB-1")
ring.add_node("DB-2")
ring.add_node("DB-3")

keys = [
    "user:101",
    "user:102",
    "user:103",
    "user:104",
    "user:105",
    "user:106"
]

print("Initial Distribution:")

for key in keys:
    print(
        key,
        "->",
        ring.get_node(key)
    )

print("\nAdding DB-4...")

ring.add_node("DB-4")

for key in keys:
    print(
        key,
        "->",
        ring.get_node(key)
    )

print("\nRemoving DB-2...")

ring.remove_node("DB-2")

for key in keys:
    print(
        key,
        "->",
        ring.get_node(key)
    )