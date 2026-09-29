# Read/Write Quorum Consistency Manager

class Replica:
    def __init__(self, replica_id):
        self.replica_id = replica_id
        self.data = {}

    def write(self, key, value):
        self.data[key] = value

    def read(self, key):
        return self.data.get(key)


class QuorumManager:
    def __init__(self, replica_count, read_quorum, write_quorum):
        if read_quorum + write_quorum <= replica_count:
            raise ValueError(
                "R + W must be greater than N"
            )

        self.replicas = [
            Replica(i)
            for i in range(replica_count)
        ]

        self.read_quorum = read_quorum
        self.write_quorum = write_quorum

    def write(self, key, value, failed_replicas=None):
        failed_replicas = failed_replicas or set()

        acknowledgements = 0

        for replica in self.replicas:
            if replica.replica_id in failed_replicas:
                continue

            replica.write(key, value)
            acknowledgements += 1

        if acknowledgements >= self.write_quorum:
            return True

        return False

    def read(self, key, failed_replicas=None):
        failed_replicas = failed_replicas or set()

        responses = []

        for replica in self.replicas:
            if replica.replica_id in failed_replicas:
                continue

            value = replica.read(key)

            if value is not None:
                responses.append(value)

            if len(responses) >= self.read_quorum:
                break

        if len(responses) < self.read_quorum:
            raise RuntimeError("Read quorum not reached")

        frequency = {}

        for value in responses:
            frequency[value] = frequency.get(value, 0) + 1

        return max(
            frequency,
            key=frequency.get
        )

    def show_replicas(self):
        for replica in self.replicas:
            print(
                f"Replica {replica.replica_id}: "
                f"{replica.data}"
            )


if __name__ == "__main__":
    manager = QuorumManager(
        replica_count=5,
        read_quorum=3,
        write_quorum=3
    )

    print("Write:", manager.write("A", 100))

    manager.show_replicas()

    print("\nRead:", manager.read("A"))

    print("\nWrite with two failed replicas:")

    success = manager.write(
        "B",
        200,
        failed_replicas={1, 4}
    )

    print("Success:", success)

    print("\nRead with one failed replica:")

    value = manager.read(
        "A",
        failed_replicas={2}
    )

    print("Value:", value)