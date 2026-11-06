# Transaction Scheduling Simulator


class TransactionScheduler:
    def __init__(self):
        self.database = {"A": 100}

        self.schedule = [
            ("T1", "READ", "A", None),
            ("T1", "WRITE", "A", 150),
            ("T2", "READ", "A", None),
            ("T2", "WRITE", "A", 200)
        ]

    def execute(self):
        print("Starting Transaction Schedule")

        for transaction, operation, key, value in self.schedule:

            if operation == "READ":
                print(
                    f"{transaction} READ {key} = "
                    f"{self.database[key]}"
                )

            elif operation == "WRITE":
                self.database[key] = value
                print(
                    f"{transaction} WRITE {key} = {value}"
                )

        print("Final Database:", self.database)


scheduler = TransactionScheduler()
scheduler.execute()
