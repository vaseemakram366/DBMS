# Distributed Concurrency Control


class DistributedConcurrencyControl:
    def __init__(self):
        self.write_timestamp = {
            "Account": 0
        }

    def write(self, transaction, timestamp, resource):
        if timestamp < self.write_timestamp[resource]:
            print(transaction, "REJECTED")
        else:
            self.write_timestamp[resource] = timestamp
            print(transaction, "WRITE SUCCESSFUL")


db = DistributedConcurrencyControl()

db.write("T1", 10, "Account")
db.write("T2", 20, "Account")
db.write("T3", 15, "Account")
z