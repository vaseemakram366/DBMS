# Distributed Data Consistency


class DistributedConsistency:
    def __init__(self):
        self.replicas = {
            "Server A": {"balance": 1000},
            "Server B": {"balance": 1000},
            "Server C": {"balance": 1000}
        }

    def update_balance(self, new_balance):
        for server in self.replicas:
            self.replicas[server]["balance"] = new_balance
            print(server, "updated to", new_balance)

    def check_consistency(self):
        balances = [
            data["balance"]
            for data in self.replicas.values()
        ]

        if len(set(balances)) == 1:
            print("All replicas are consistent")
        else:
            print("Replicas are inconsistent")


db = DistributedConsistency()

db.update_balance(1500)

print()
db.check_consistency()
