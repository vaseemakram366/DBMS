# Transaction Recovery Property Fuzz Tester


import random


def analyze_schedule(schedule):
    last_writer = {}
    committed = set()
    commit_index = {}
    dependencies = set()

    dirty_reads = []
    strict_violations = []

    for index, (op, tid, item) in enumerate(schedule):

        if op == "C":
            committed.add(tid)
            commit_index[tid] = index
            continue

        previous_writer = last_writer.get(item)

        # Strictness: no other transaction may read/write
        # an item whose latest writer is still uncommitted.
        if (
            previous_writer is not None
            and previous_writer != tid
            and previous_writer not in committed
        ):
            strict_violations.append(
                (index, op, tid, item, previous_writer)
            )

        if op == "R":
            if previous_writer is not None and previous_writer != tid:
                dependencies.add((previous_writer, tid))

                # Cascadelessness: reads must not use
                # another transaction's uncommitted write.
                if previous_writer not in committed:
                    dirty_reads.append(
                        (index, tid, item, previous_writer)
                    )

        elif op == "W":
            last_writer[item] = tid

    # Recoverability: a reader must not commit before
    # the transaction whose value it read.
    recovery_violations = [
        (writer, reader)
        for writer, reader in sorted(dependencies)
        if commit_index[reader] < commit_index[writer]
    ]

    return {
        "recoverable": not recovery_violations,
        "cascadeless": not dirty_reads,
        "strict": not strict_violations,
        "recovery_violations": recovery_violations,
        "dirty_reads": dirty_reads,
        "strict_violations": strict_violations,
    }


def generate_schedule(rng, tx_count=3, items=("A", "B", "C")):
    # Preserve each transaction's own operation order.
    queues = {}

    for tid in range(1, tx_count + 1):
        operations = []

        for _ in range(rng.randint(2, 4)):
            op = rng.choice(("R", "W"))
            item = rng.choice(items)
            operations.append((op, tid, item))

        # Every generated transaction commits exactly once.
        operations.append(("C", tid, None))
        queues[tid] = operations

    # Randomly interleave the transaction operations.
    schedule = []

    while any(queues.values()):
        available = [
            tid for tid, queue in queues.items() if queue
        ]
        tid = rng.choice(available)
        schedule.append(queues[tid].pop(0))

    return schedule


def fuzz_test(test_count=500):
    rng = random.Random(7)

    totals = {
        "recoverable": 0,
        "cascadeless": 0,
        "strict": 0,
    }

    invariant_failures = 0

    for _ in range(test_count):
        schedule = generate_schedule(rng)
        result = analyze_schedule(schedule)

        for property_name in totals:
            totals[property_name] += result[property_name]

        # Strict implies cascadeless.
        # Cascadeless implies recoverable.
        if (
            (result["strict"] and not result["cascadeless"])
            or
            (result["cascadeless"] and not result["recoverable"])
        ):
            invariant_failures += 1

    print("Total schedules tested:", test_count)
    print("Recoverable schedules:", totals["recoverable"])
    print("Cascadeless schedules:", totals["cascadeless"])
    print("Strict schedules:", totals["strict"])
    print("Invariant failures:", invariant_failures)

    if invariant_failures == 0:
        print("Result: All tested invariants passed.")
    else:
        print("Result: Investigate the analyzer or test cases.")


if __name__ == "__main__":
    fuzz_test()
