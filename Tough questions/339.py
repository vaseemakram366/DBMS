# Cascadeless Schedule Checker


class CascadelessSchedule:
    def __init__(self, schedule):
        self.schedule = schedule

    def check(self):
        last_writer = {}
        committed = set()

        for tx, op, item in self.schedule:
            if op == "W":
                last_writer[item] = tx

            elif op == "R":
                writer = last_writer.get(item)

                if writer is not None and writer != tx:
                    if writer not in committed:
                        print("Not Cascadeless Schedule")
                        print(f"{tx} read uncommitted data from {writer}")
                        return

            elif op == "C":
                committed.add(tx)

        print("Cascadeless Schedule")


schedule = [
    ("T1", "W", "A"),
    ("T1", "C", None),
    ("T2", "R", "A"),
    ("T2", "C", None)
]

obj = CascadelessSchedule(schedule)
obj.check()
