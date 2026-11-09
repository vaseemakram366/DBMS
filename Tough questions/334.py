# Multiversion Concurrency Control (MVCC)


class MVCC:
    def __init__(self):
        self.versions = {
            "A": [(100, 0)]
        }

    def read(self, item, timestamp):
        valid_versions = [
            (value, ts)
            for value, ts in self.versions[item]
            if ts <= timestamp
        ]

        if not valid_versions:
            print("No visible version found")
            return

        value, ts = max(valid_versions, key=lambda x: x[1])

        print(f"Read at time {timestamp}: {item} = {value}")

    def write(self, item, value, timestamp):
        self.versions[item].append((value, timestamp))
        print(f"New version created: {item} = {value}")


db = MVCC()

db.write("A", 200, 5)

db.read("A", 3)
db.read("A", 5)

print("All Versions:", db.versions["A"])
