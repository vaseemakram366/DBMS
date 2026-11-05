# Eventual Consistency Simulator


class EventualConsistency:
    def __init__(self):
        self.replicas = {
            "Server A": 100,
            "Server B": 100,
            "Server C": 100
        }

    def update_server(self, server, value):
        self.replicas[server] = value
        print(server, "updated to", value)

    def synchronize(self):
        latest_value = self.replicas["Server A"]

        for server in self.replicas:
            self.replicas[server] = latest_value

        print("\nSynchronization completed")
        print("Replica values:", self.replicas)

    def check_consistency(self):
        if len(set(self.replicas.values())) == 1:
            print("All replicas are consistent")
        else:
            print("Replicas are not yet consistent")


db = EventualConsistency()

db.update_server("Server A", 500)

db.check_consistency()

db.synchronize()

db.check_consistency()
feat: implement eventual consistency simulator