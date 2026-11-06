# Recoverable Schedule Checker


class RecoverableSchedule:
    def __init__(self):
        self.schedule = [
            ("T1", "WRITE", "A"),
            ("T2", "READ", "A"),
            ("T1", "COMMIT", None),
            ("T2", "COMMIT", None)
        ]

    def check(self):
        last_writer = {}
        commit_order = []
        dependencies = []

        for transaction, operation, data in self.schedule:

            if operation == "WRITE":
                last_writer[data] = transaction

            elif operation == "READ":
                if data in last_writer:
                    writer = last_writer[data]
                    if writer != transaction:
                        dependencies.append((writer, transaction))

            elif operation == "COMMIT":
                commit_order.append(transaction)

        for writer, reader in dependencies:
            if writer in commit_order and reader in commit_order:
                if commit_order.index(writer) > commit_order.index(reader):
                    print("Schedule is NOT Recoverable")
                    return

        print("Schedule is Recoverable")


schedule = RecoverableSchedule()
schedule.check()
