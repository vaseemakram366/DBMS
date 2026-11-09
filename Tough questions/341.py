# Conflict Detection Between Transactions


class ConflictDetection:
    def __init__(self, schedule):
        self.schedule = schedule

    def detect(self):
        conflicts = []

        for i in range(len(self.schedule)):
            tx1, op1, item1 = self.schedule[i]

            for j in range(i + 1, len(self.schedule)):
                tx2, op2, item2 = self.schedule[j]

                if tx1 == tx2:
                    continue

                if item1 != item2:
                    continue

                if op1 == "W" or op2 == "W":
                    conflicts.append(
                        (tx1, op1, tx2, op2, item1)
                    )

        if not conflicts:
            print("No Conflicts Found!")
            return

        print("Conflicts Detected:")

        for tx1, op1, tx2, op2, item in conflicts:
            print(
                f"{tx1}({op1}) -> {tx2}({op2}) on {item}"
            )


schedule = [
    ("T1", "R", "A"),
    ("T2", "W", "A"),
    ("T1", "W", "B"),
    ("T2", "R", "B"),
    ("T1", "R", "C"),
    ("T2", "R", "C")
]

obj = ConflictDetection(schedule)
obj.detect()
