# Strict Schedule Checker


class StrictScheduleChecker:
    def __init__(self):
        self.schedule = [
            ("T1", "WRITE", "A"),
            ("T2", "READ", "A"),
            ("T1", "COMMIT", None),
            ("T2", "READ", "A")
        ]

    def check(self):
        active_writers = {}

        for transaction, operation, data in self.schedule:

            if operation == "WRITE":
                active_writers[data] = transaction

            elif operation == "READ":
                if data in active_writers:
                    if active_writers[data] != transaction:
                        print("Schedule is NOT Strict")
                        return

            elif operation == "COMMIT" or operation == "ABORT":
                for item in list(active_writers):
                    if active_writers[item] == transaction:
                        del active_writers[item]

        print("Schedule is Strict")


checker = StrictScheduleChecker()
checker.check()
