# Recoverable, Cascadeless & Strict Schedule Checker

from collections import defaultdict


class ScheduleChecker:
    def __init__(self, schedule):
        self.schedule = schedule
        self.read_from = defaultdict(set)
        self.writes = defaultdict(set)
        self.committed = set()

    def analyze(self):
        last_write = {}

        for i, event in enumerate(self.schedule):
            transaction, operation, item = event

            if operation == "W":
                self.writes[transaction].add(item)
                last_write[item] = transaction

            elif operation == "R":
                if item in last_write:
                    writer = last_write[item]

                    if writer != transaction:
                        self.read_from[transaction].add(writer)

            elif operation == "C":
                self.committed.add(transaction)

    def is_recoverable(self):
        commit_position = {}

        for i, event in enumerate(self.schedule):
            transaction, operation, item = event

            if operation == "C":
                commit_position[transaction] = i

        for reader, writers in self.read_from.items():
            for writer in writers:
                if writer not in commit_position:
                    return False

                if reader not in commit_position:
                    return False

                if commit_position[writer] > commit_position[reader]:
                    return False

        return True

    def is_cascadeless(self):
        active_writes = {}

        for transaction, operation, item in self.schedule:
            if operation == "W":
                active_writes[item] = transaction

            elif operation == "R":
                if item in active_writes:
                    writer = active_writes[item]

                    if writer != transaction and writer not in self.committed:
                        return False

            elif operation == "C":
                to_remove = []

                for item, writer in active_writes.items():
                    if writer == transaction:
                        to_remove.append(item)

                for item in to_remove:
                    del active_writes[item]

        return True

    def is_strict(self):
        active_writes = {}

        for transaction, operation, item in self.schedule:
            if operation == "W":
                if item in active_writes:
                    return False

                active_writes[item] = transaction

            elif operation == "R":
                if item in active_writes:
                    writer = active_writes[item]

                    if writer != transaction:
                        return False

            elif operation == "C":
                to_remove = []

                for item, writer in active_writes.items():
                    if writer == transaction:
                        to_remove.append(item)

                for item in to_remove:
                    del active_writes[item]

        return True

    def check(self):
        self.analyze()

        recoverable = self.is_recoverable()
        cascadeless = self.is_cascadeless()
        strict = self.is_strict()

        return {
            "Recoverable": recoverable,
            "Cascadeless": cascadeless,
            "Strict": strict
        }


schedule = [
    ("T1", "W", "A"),
    ("T1", "C", None),
    ("T2", "R", "A"),
    ("T2", "W", "B"),
    ("T2", "C", None)
]

checker = ScheduleChecker(schedule)

result = checker.check()

for property_name, value in result.items():
    print(f"{property_name}: {value}")