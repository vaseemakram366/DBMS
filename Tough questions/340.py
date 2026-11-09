# Strict Schedule Checker


class StrictSchedule:
    def __init__(self, schedule):
        self.schedule = schedule

    def check(self):
        active_writers = {}

        for tx, op, item in self.schedule:
            if op == "W":
                writer = active_writers.get(item)

                if writer is not None and writer != tx:
                    print("Not a Strict Schedule")
                    print(f"{tx} accessed {item} before {writer} completed")
                    return

                active_writers[item] = tx

            elif op == "R":
                writer = active_writers.get(item)

                if writer is not None and writer != tx:
                    print("Not a Strict Schedule")
                    print(f"{tx} read {item} before {writer} completed")
                    return

            elif op in ("C", "A"):
                for item_name, writer in list(active_writers.items()):
                    if writer == tx:
                        del active_writers[item_name]

        print("Strict Schedule")


schedule = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T1", "C", None)
]

obj = StrictSchedule(schedule)
obj.check()
