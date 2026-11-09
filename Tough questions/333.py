# Optimistic Concurrency Control (OCC)


class OptimisticConcurrencyControl:
    def __init__(self):
        self.database = {"A": 100}
        self.committed = {}

    def execute(self, transaction, new_value, start_time):
        print(f"{transaction}: Read Phase")

        local_value = new_value

        print(f"{transaction}: Validation Phase")

        for tx, commit_time in self.committed.items():
            if commit_time > start_time:
                print(f"{transaction}: Validation Failed!")
                return

        print(f"{transaction}: Validation Successful")

        self.database["A"] = local_value
        self.committed[transaction] = start_time + 1

        print(f"{transaction}: Write Phase")
        print("Database:", self.database)


db = OptimisticConcurrencyControl()

db.execute("T1", 200, 1)
db.execute("T2", 300, 1)
