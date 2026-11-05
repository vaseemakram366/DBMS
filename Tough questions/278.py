# Distributed Log Management


class DistributedLogManager:
    def __init__(self):
        self.logs = {
            "Server A": [],
            "Server B": [],
            "Server C": []
        }

    def add_log(self, server, message):
        if server in self.logs:
            self.logs[server].append(message)
            print(server, "logged:", message)

    def display_logs(self):
        print("\nAll Distributed Logs:")

        for server, entries in self.logs.items():
            print(server, ":", entries)


db = DistributedLogManager()

db.add_log("Server A", "Transaction Started")
db.add_log("Server B", "Data Updated")
db.add_log("Server C", "Transaction Committed")

db.display_logs()
