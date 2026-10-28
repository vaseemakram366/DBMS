# Transaction Schedule Property-Based Tester


import random


def analyze_schedule(schedule):
    last_writer = {}
    active_writers = {}
    committed = set()
    commit_index = {}
    dependencies = set()
    dirty_reads = False
    strict_violations = False

    for index, (op, tid, item) in enumerate(schedule):
        if op == "C":
            committed.add(tid)
            commit_index[tid] = index

            for writers in active_writers.values():
                writers.discard(tid)
            continue

        writers = active_writers.setdefault(item, set())

        if any(writer != tid for writer in writers):
            strict_violations = True

        if op == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != tid:
                dependencies.add((writer, tid))

                if writer not in committed:
                    dirty_reads = True

        elif op == "W":
            last_writer[item] = tid
            writers.add(tid)

    recoverable = all(
        commit_index[writer] < commit_index[reader]
        for writer, reader in dependencies
    )

    return {
        "recoverable": recoverable,
        "cascadeless": not dirty_reads,
        "strict": not strict_violations,
    }


def generate_schedule(rng, transaction_count=4):
    queues = {}

    for tid in range(1, transaction_count + 1):
        operations = []

        for _ in range(rng.randint(2, 5)):
            op = rng.choice(["R", "W"])
            item = rng.choice(["A", "B", "C"])
            operations.append((op, tid, item))

        operations.append(("C", tid, None))
        queues[tid] = operations

    schedule = []

    while any(queues.values()):
        available = [
            tid for tid in queues if queues[tid]
        ]
        tid = rng.choice(available)
        schedule.append(queues[tid].pop(0))

    return schedule


def valid_transaction_lifecycle(schedule, count):
    finished = set()
    commits = {tid: 0 for tid in range(1, count + 1)}

    for op, tid, item in schedule:
        if tid in finished:
            return False

        if op == "C":
            commits[tid] += 1
            finished.add(tid)

    return (
        len(finished) == count
        and all(value == 1 for value in commits.values())
    )


def run_property_tests(test_count=1000):
    rng = random.Random(51)
    failures = 0

    for test_number in range(1, test_count + 1):
        schedule = generate_schedule(rng)
        result = analyze_schedule(schedule)

        lifecycle_ok = valid_transaction_lifecycle(
            schedule, 4
        )

        # Property 1: Strict implies cascadeless.
        property_1 = (
            not result["strict"]
            or result["cascadeless"]
        )

        # Property 2: Cascadeless implies recoverable.
        property_2 = (
            not result["cascadeless"]
            or result["recoverable"]
        )

        if not (
            lifecycle_ok
            and property_1
            and property_2
        ):
            failures += 1
            print("Failure in test:", test_number)
            print("Schedule:", schedule)
            print("Results:", result)
            break

    print("Schedules tested:", test_count)
    print("Invariant violations:", failures)

    if failures == 0:
        print("Result: All property checks passed.")
    else:
        print("Result: A property failed; investigate the bug.")


if __name__ == "__main__":
    run_property_tests()
