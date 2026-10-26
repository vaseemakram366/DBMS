# Transaction Schedule Fuzz Tester


import random
from collections import defaultdict


def generate_schedule(num_transactions=3, seed=None):
    rng = random.Random(seed)
    schedule = []
    items = ["A", "B", "C"]

    for i in range(1, num_transactions + 1):
        tx = f"T{i}"
        operations = []

        for _ in range(rng.randint(1, 4)):
            op = rng.choice(["R", "W"])
            item = rng.choice(items)
            operations.append((tx, op, item))

        operations.append((tx, "C", ""))

        # Preserve each transaction's operation order.
        schedule.append(operations)

    result = []

    while any(schedule):
        available = [i for i, ops in enumerate(schedule) if ops]
        chosen = rng.choice(available)
        result.append(schedule[chosen].pop(0))

    return result


def validate_structure(schedule):
    states = defaultdict(lambda: "ACTIVE")
    errors = []

    for index, (tx, op, item) in enumerate(schedule):
        if op not in {"R", "W", "C", "A"}:
            errors.append(f"Operation {index}: invalid operation {op}")
            continue

        if states[tx] != "ACTIVE":
            errors.append(
                f"Operation {index}: {tx} operates after termination"
            )
            continue

        if op in {"R", "W"} and not item:
            errors.append(
                f"Operation {index}: missing data item"
            )

        elif op == "C":
            states[tx] = "COMMITTED"

        elif op == "A":
            states[tx] = "ABORTED"

    for tx, state in states.items():
        if state == "ACTIVE":
            errors.append(f"{tx} has no commit or abort")

    return errors


def fuzz_test(iterations=1000):
    valid_count = 0
    invalid_count = 0

    for seed in range(iterations):
        schedule = generate_schedule(
            num_transactions=3,
            seed=seed
        )

        errors = validate_structure(schedule)

        if errors:
            invalid_count += 1
            print(f"\nInvalid schedule (seed={seed}):")
            for error in errors:
                print(" -", error)

            if invalid_count >= 3:
                break
        else:
            valid_count += 1

    print("\nFuzz Testing Summary")
    print("--------------------")
    print("Valid schedules:", valid_count)
    print("Invalid schedules found:", invalid_count)


if __name__ == "__main__":
    fuzz_test()
