# Read-Write Consistency Simulation


class ReadWriteConsistency:
    def __init__(self):
        self.primary = {"balance": 1000}

        self.replicas = {
            "Server B": {"balance": 1000},
            "Server C": {"balance": 1000}
        }

    def write(self, value):
        self.primary["balance"] = value
        print("Write successful:", value)

    def synchronize(self):
        for server in self.replicas:
            self.replicas[server] = self.primary.copy()

        print("Replicas synchronized")

    def read(self, server):
        if server == "Primary":
            print("Read from Primary:", self.primary)
        elif server in self.replicas:
            print("Read from", server, ":", self.replicas[server])


db = ReadWriteConsistency()

db.write(2000)
db.synchronize()

db.read("Primary")
db.read("Server B")
db.read("Server C")
