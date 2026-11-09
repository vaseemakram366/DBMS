# Recoverable Schedule Checker


class RecoverableSchedule:
    def __init__(self, schedule):
        self.schedule = schedule

    def check(self):
        last_writer = {}
        dependencies = []

        commit_time = {}

        for index, operation in enumerate(self.schedule):
            tx, op, item = operation

            if op == "W":
                last_writer[item] = tx

            elif op == "R":
                writer = last_writer.get(item)

                if writer is not None and writer != tx:
                    dependencies.append((writer, tx))

            elif op == "C":
                commit_time[tx] = index

        for writer, reader in dependencies:
            if reader in commit_time:
                if writer not in commit_time:
                    print("Not Recoverable")
                    return

                if commit_time[writer] > commit_time[reader]:
                    print("Not Recoverable")
                    return

        print("Recoverable Schedule")


schedule = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T1", "C", None),
    ("T2", "C", None)
]

obj = RecoverableSchedule(schedule)
obj.check()
