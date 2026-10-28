# Transaction Schedule Recovery Analyzer


class RecoveryAnalyzer:
    def __init__(self, schedule):
        self.schedule = schedule

    def analyze(self):
        committed = set()
        aborted = set()
        last_writer = {}
        dirty_reads = []
        dirty_writes = []
        read_from = []
        recoverable = True
        cascadeless = True
        strict = True
        violations = []

        for position, event in enumerate(self.schedule, start=1):
            action = event[0]

            if action in ("R", "W"):
                _, transaction, item = event

                if transaction in committed or transaction in aborted:
                    violations.append(
                        f"T{transaction} performs {action} after termination."
                    )
                    continue

                writer = last_writer.get(item)

                if action == "R":
                    if writer is not None and writer != transaction:
                        read_from.append((writer, transaction, item))

                        if writer not in committed:
                            dirty_reads.append(
                                (position, writer, transaction, item)
                            )
                            cascadeless = False
                            strict = False

                            if transaction in committed:
                                recoverable = False

                elif action == "W":
                    if writer is not None and writer != transaction:
                        if writer not in committed:
                            dirty_writes.append(
                                (position, writer, transaction, item)
                            )
                            strict = False

                    last_writer[item] = transaction

            elif action == "C":
                transaction = event[1]

                if transaction in aborted:
                    violations.append(
                        f"T{transaction} commits after abort."
                    )
                committed.add(transaction)

                for writer, reader, item in read_from:
                    if reader == transaction and writer not in committed:
                        recoverable = False

            elif action == "A":
                transaction = event[1]
                aborted.add(transaction)

                if transaction in committed:
                    violations.append(
                        f"T{transaction} aborts after commit."
                    )

            else:
                raise ValueError(f"Unknown event: {event}")

        return {
            "dirty_reads": dirty_reads,
            "dirty_writes": dirty_writes,
            "recoverable": recoverable,
            "cascadeless": cascadeless,
            "strict": strict,
            "violations": violations,
        }


if __name__ == "__main__":
    schedule = [
        ("W", 1, "A"),
        ("R", 2, "A"),
        ("C", 1),
        ("C", 2),
    ]

    analyzer = RecoveryAnalyzer(schedule)
    result = analyzer.analyze()

    print("Schedule:")
    for event in schedule:
        print(event)

    print("\nDirty reads:", result["dirty_reads"])
    print("Dirty writes:", result["dirty_writes"])
    print("Recoverable:", result["recoverable"])
    print("Cascadeless:", result["cascadeless"])
    print("Strict:", result["strict"])
    print("Violations:", result["violations"])
