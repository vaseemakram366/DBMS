# Transaction Recovery Schedule Validator


def validate_schedule(schedule):
    errors = []
    transactions = set()
    committed = set()
    commit_index = {}
    last_writer = {}
    active_writers = {}
    dependencies = set()
    dirty_reads = []
    strict_violations = []

    for index, event in enumerate(schedule):
        if not isinstance(event, tuple) or len(event) != 3:
            errors.append(f"Event {index}: invalid event format")
            continue

        op, tid, item = event

        if op not in {"R", "W", "C"}:
            errors.append(f"Event {index}: invalid operation {op}")
            continue

        if not isinstance(tid, int) or tid <= 0:
            errors.append(f"Event {index}: invalid transaction ID")
            continue

        transactions.add(tid)

        if tid in committed:
            errors.append(
                f"Event {index}: T{tid} operates after commit"
            )
            continue

        if op == "C":
            if item is not None:
                errors.append(
                    f"Event {index}: commit item must be None"
                )

            committed.add(tid)
            commit_index[tid] = index

            for writers in active_writers.values():
                writers.discard(tid)

            continue

        if not isinstance(item, str) or not item:
            errors.append(f"Event {index}: invalid data item")
            continue

        writers = active_writers.setdefault(item, set())

        if any(writer != tid for writer in writers):
            strict_violations.append((index, op, tid, item))

        if op == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != tid:
                dependencies.add((writer, tid))

                if writer not in committed:
                    dirty_reads.append(
                        (index, tid, item, writer)
                    )

        elif op == "W":
            last_writer[item] = tid
            writers.add(tid)

    # Require every transaction appearing in the schedule to commit.
    for tid in sorted(transactions - committed):
        errors.append(f"T{tid} has no commit")

    recovery_violations = []

    for writer, reader in sorted(dependencies):
        if (
            writer in commit_index
            and reader in commit_index
            and commit_index[reader] < commit_index[writer]
        ):
            recovery_violations.append((writer, reader))

    valid = not errors

    print("SCHEDULE VALIDATION REPORT")
    print("=" * 35)
    print("Structurally valid:", valid)
    print("Recoverable:", not recovery_violations and valid)
    print("Cascadeless:", not dirty_reads and valid)
    print("Strict:", not strict_violations and valid)

    print("\nStructural errors:")
    if errors:
        for error in errors:
            print("-", error)
    else:
        print("None")

    print("\nDirty reads:", dirty_reads)
    print("Recovery violations:", recovery_violations)
    print("Strictness violations:", strict_violations)


def main():
    schedule = [
        ("W", 1, "A"),
        ("R", 2, "A"),
        ("C", 2, None),
        ("C", 1, None),
    ]

    validate_schedule(schedule)


if __name__ == "__main__":
    main()
