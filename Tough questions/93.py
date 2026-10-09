# Read Repair Mechanism for Distributed Databases

class Replica:
    def __init__(self, replica_id):
        self.replica_id = replica_id
        self.data = {}

    def write(self, key, value, version):
        current = self.data.get(key)

        if current is None or version > current["version"]:
            self.data[key] = {
                "value": value,
                "version": version
            }

    def read(self, key):
        return self.data.get(key)


class DistributedDatabase:
    def __init__(self, replica_count=3):
        self.replicas = [
            Replica(i) for i in range(replica_count)
        ]

    def write(self, key, value, version):
        for replica in self.replicas:
            replica.write(key, value, version)

    def read_repair(self, key):
        records = [
            replica.read(key)
            for replica in self.replicas
        ]

        existing = [r for r in records if r is not None]

        if not existing:
            return None

        latest = max(
            existing,
            key=lambda record: record["version"]
        )

        for replica in self.replicas:
            replica.write(
                key,
                latest["value"],
                latest["version"]
            )

        return latest["value"]

    def show_replicas(self, key):
        for replica in self.replicas:
            print(
                f"Replica {replica.replica_id}:",
                replica.read(key)
            )


db = DistributedDatabase()

db.write("user:101", {"age": 20}, 1)

# Simulate a newer write reaching only two replicas.
db.replicas[0].write("user:101", {"age": 22}, 2)
db.replicas[1].write("user:101", {"age": 22}, 2)

print("Before repair:")
db.show_replicas("user:101")

db.read_repair("user:101")

print("\nAfter repair:")
db.show_replicas("user:101")