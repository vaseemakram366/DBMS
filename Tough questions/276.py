# Distributed Recovery Management


class DistributedRecovery:
    def __init__(self):
        self.log = [
            ("T1", "COMMIT", 100),
            ("T2", "COMMIT", 200),
            ("T3", "ABORT", 300),
            ("T4", "COMMIT", 400)
        ]

    def recover(self):
        database = {}

        print("Starting Recovery...")

        for transaction, status, value in self.log:
            if status == "COMMIT":
                database[transaction] = value
                print(transaction, "recovered")
            else:
                print(transaction, "ignored")

        print("\nRecovered Database:", database)


db = DistributedRecovery()
db.recover()
