# Transaction Schedule Mutation Tester


def analyze_schedule(schedule):
    last_writer = {}
    active_writers = {}
    committed = set()
    commit_index = {}
    dependencies = set()

    for index, (op, tid, item) in enumerate(schedule):
        if op == "C":
            committed.add(tid)
            commit_index[tid] = index

            for writers in active_writers.values():
                writers.discard(tid)

            continue

        writers = active_writers.setdefault(item, set())

        # Strictness check: another transaction must not
        # read/write an item with an uncommitted write.
        if any(writer != tid for writer in writers):
            pass
        else:
            pass

        strict_violation = any(writer != tid for writer in writers)

        if op == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != tid:
                dependencies.add((writer, tid))

        elif op == "W":
            last_writer[item] = tid
            writers.add(tid)

    # Reconstruct read-from dependencies and check dirty reads.
    last_writer = {}
    active_writers = {}
    dirty_reads = []
    strict_violations = []
    dependencies = set()

    for index, (op, tid, item) in enumerate(schedule):
        if op == "C":
            committed.add(tid)
            for writers in active_writers.values():
                writers.discard(tid)
            continue

        writers = active_writers.setdefault(item, set())

        if any(writer != tid for writer in writers):
            strict_violations.append((index, op, tid, item))

        if op == "R":
            writer = last_writer.get(item)
            if writer is not None and writer != tid:
                dependencies.add((writer, tid))
                if writer not in committed:
                    dirty_reads.append((index, tid, item, writer))

        elif op == "W":
            last_writer[item] = tid
            writers.add(tid)

    recovery_violations = []
    for writer, reader in dependencies:
        if commit_index[reader] < commit_index[writer]:
            recovery_violations.append((writer, reader))

    return {
        "recoverable": not recovery_violations,
        "cascadeless": not dirty_reads,
        "strict": not strict_violations,
    }


def show_result(name, schedule):
    result = analyze_schedule(schedule)

    print(name)
    print("  Schedule:", schedule)
    print("  Recoverable:", result["recoverable"])
    print("  Cascadeless:", result["cascadeless"])
    print("  Strict:", result["strict"])
    print()


def main():
    original = [
        ("W", 1, "A"),
        ("R", 2, "A"),
        ("C", 2, None),
        ("C", 1, None),
    ]

    # Mutation 1: Swap the commit order.
    mutation_1 = [
        ("W", 1, "A"),
        ("R", 2, "A"),
        ("C", 1, None),
        ("C", 2, None),
    ]

    # Mutation 2: Commit T1 before T2 reads A.
    mutation_2 = [
        ("W", 1, "A"),
        ("C", 1, None),
        ("R", 2, "A"),
        ("C", 2, None),
    ]

    show_result("Original", original)
    show_result("Mutation 1: Swap commits", mutation_1)
    show_result("Mutation 2: Move writer commit earlier", mutation_2)


if __name__ == "__main__":
    main()
