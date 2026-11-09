# Schedule Equivalence Checker


class ScheduleEquivalence:
    def __init__(self, schedule1, schedule2):
        self.schedule1 = schedule1
        self.schedule2 = schedule2

    def check(self):
        operations1 = {}
        operations2 = {}

        for tx, op, item in self.schedule1:
            operations1.setdefault(tx, []).append((op, item))

        for tx, op, item in self.schedule2:
            operations2.setdefault(tx, []).append((op, item))

        if operations1 == operations2:
            print("Schedules are Equivalent")
        else:
            print("Schedules are Not Equivalent")


schedule1 = [
    ("T1", "R", "A"),
    ("T1", "W", "B"),
    ("T2", "R", "C"),
    ("T2", "W", "D")
]

schedule2 = [
    ("T2", "R", "C"),
    ("T1", "R", "A"),
    ("T2", "W", "D"),
    ("T1", "W", "B")
]

obj = ScheduleEquivalence(schedule1, schedule2)
obj.check()
