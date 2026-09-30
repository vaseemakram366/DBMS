# Vector Clock Conflict Resolution

class VectorClock:
    def __init__(self, clock=None):
        self.clock = clock.copy() if clock else {}

    def increment(self, node):
        self.clock[node] = self.clock.get(node, 0) + 1

    def merge(self, other):
        nodes = set(self.clock) | set(other.clock)

        for node in nodes:
            self.clock[node] = max(
                self.clock.get(node, 0),
                other.clock.get(node, 0)
            )

    def happens_before(self, other):
        nodes = set(self.clock) | set(other.clock)

        less = False

        for node in nodes:
            a = self.clock.get(node, 0)
            b = other.clock.get(node, 0)

            if a > b:
                return False

            if a < b:
                less = True

        return less

    def concurrent_with(self, other):
        return (
            not self.happens_before(other)
            and not other.happens_before(self)
        )

    def copy(self):
        return VectorClock(self.clock)

    def __str__(self):
        return str(self.clock)


class Version:
    def __init__(self, value, clock):
        self.value = value
        self.clock = clock.copy()


class Replica:
    def __init__(self, replica_id):
        self.replica_id = replica_id
        self.clock = VectorClock()
        self.data = {}

    def write(self, key, value):
        self.clock.increment(self.replica_id)

        self.data[key] = Version(
            value,
            self.clock
        )

    def receive(self, key, version):
        self.clock.merge(version.clock)

        if key not in self.data:
            self.data[key] = Version(
                version.value,
                version.clock
            )
            return

        current = self.data[key]

        if current.clock.happens_before(version.clock):
            self.data[key] = Version(
                version.value,
                version.clock
            )

        elif version.clock.concurrent_with(current.clock):
            print(
                f"Conflict detected for key '{key}': "
                f"{current.value} vs {version.value}"
            )

    def show(self):
        print(f"\nReplica {self.replica_id}")

        for key, version in self.data.items():
            print(
                f"{key} = {version.value}, "
                f"clock = {version.clock}"
            )


if __name__ == "__main__":
    replica_a = Replica("A")
    replica_b = Replica("B")

    replica_a.write("user", "Aman")
    replica_b.write("user", "Rahul")

    print("Initial independent writes:")
    replica_a.show()
    replica_b.show()

    print("\nSending A's version to B:")
    replica_b.receive(
        "user",
        replica_a.data["user"]
    )

    print("\nSending B's version to A:")
    replica_a.receive(
        "user",
        replica_b.data["user"]
    )

    replica_a.show()
    replica_b.show()