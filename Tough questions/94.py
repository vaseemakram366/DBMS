# CRDT-Based Replicated Database

class GCounter:
    def __init__(self, replica_id, replica_count):
        self.replica_id = replica_id
        self.counts = [0] * replica_count

    def increment(self, amount=1):
        if amount > 0:
            self.counts[self.replica_id] += amount

    def value(self):
        return sum(self.counts)

    def merge(self, other):
        if len(self.counts) != len(other.counts):
            raise ValueError("Replica count mismatch")

        self.counts = [
            max(a, b)
            for a, b in zip(self.counts, other.counts)
        ]


class DistributedDatabase:
    def __init__(self, replica_count):
        self.replicas = [
            GCounter(i, replica_count)
            for i in range(replica_count)
        ]

    def increment(self, replica_id, amount=1):
        self.replicas[replica_id].increment(amount)

    def synchronize(self):
        for i in range(len(self.replicas)):
            for j in range(len(self.replicas)):
                if i != j:
                    self.replicas[i].merge(
                        self.replicas[j]
                    )

    def show(self):
        for replica in self.replicas:
            print(
                f"Replica {replica.replica_id}: "
                f"counts={replica.counts}, "
                f"value={replica.value()}"
            )


db = DistributedDatabase(3)

db.increment(0, 5)
db.increment(1, 3)
db.increment(2, 7)

print("Before synchronization:")
db.show()

db.synchronize()

print("\nAfter synchronization:")
db.show()