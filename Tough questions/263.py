# Consistent Hashing Basics


import hashlib


class ConsistentHashing:
    def __init__(self):
        self.ring = {}

    def get_hash(self, value):
        result = hashlib.md5(
            str(value).encode()
        ).hexdigest()

        return int(result, 16)

    def add_server(self, server):
        position = self.get_hash(server)
        self.ring[position] = server
        print(f"Server {server} added")

    def get_server(self, key):
        if not self.ring:
            print("No servers available")
            return

        key_position = self.get_hash(key)

        positions = sorted(self.ring)

        for position in positions:
            if position >= key_position:
                return self.ring[position]

        return self.ring[positions[0]]

    def show_ring(self):
        for position in sorted(self.ring):
            print(position, "->", self.ring[position])


cluster = ConsistentHashing()

cluster.add_server("Server-A")
cluster.add_server("Server-B")
cluster.add_server("Server-C")

for key in ["Alice", "Bob", "Charlie"]:
    server = cluster.get_server(key)
    print(f"{key} assigned to {server}")
