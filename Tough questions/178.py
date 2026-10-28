# Transaction Schedule Minimal Counterexample Finder


def is_recoverable(schedule):
    last_writer = {}
    dependencies = set()
    commit_index = {}

    for index, (op, tid, item) in enumerate(schedule):
        if op == "C":
            commit_index[tid] = index
        elif op == "W":
            last_writer[item] = tid
        elif op == "R":
            writer = last_writer.get(item)
            if writer is not None and writer != tid:
                dependencies.add((writer, tid))

    for writer, reader in dependencies:
        if writer not in commit_index or reader not in commit_index:
            return False

        if commit_index[reader] < commit_index[writer]:
            return False

    return True


def preserves_failure(schedule, failure_predicate):
    return failure_predicate(schedule)


def minimize_schedule(schedule, failure_predicate):
    current = schedule[:]
    changed = True

    while changed:
        changed = False

        for index in range(len(current)):
            candidate = current[:index] + current[index + 1:]

            if preserves_failure(candidate, failure_predicate):
                current = candidate
                changed = True
                break

    return current


def print_schedule(schedule):
    if not schedule:
        print("  <empty schedule>")
        return

    for index, event in enumerate(schedule, start=1):
        print(f"  {index}. {event}")


def main():
    schedule = [
        ("W", 1, "A"),
        ("W", 3, "B"),
        ("R", 2, "A"),
        ("R", 4, "B"),
        ("C", 2, None),
        ("C", 4, None),
        ("C", 1, None),
        ("C", 3, None),
    ]

    # We want a schedule that remains non-recoverable.
    failure_predicate = lambda s: not is_recoverable(s)

    print("Original schedule:")
    print_schedule(schedule)
    print("Recoverable:", is_recoverable(schedule))

    minimized = minimize_schedule(
        schedule, failure_predicate
    )

    print("\nMinimized counterexample:")
    print_schedule(minimized)
    print("Recoverable:", is_recoverable(minimized))


if __name__ == "__main__":
    main()
