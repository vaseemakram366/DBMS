# Transaction Schedule Equivalence Checker


from itertools import combinations


def get_operations_by_transaction(schedule):
    return {
        transaction
        for transaction, _, _ in schedule
    }


def are_conflicting(op1, op2):
    t1, action1, item1 = op1
    t2, action2, item2 = op2

    return (
        t1 != t2
        and item1 == item2
        and (action1 == "W" or action2 == "W")
    )


def get_conflict_order(schedule):
    conflict_order = set()

    for i, op1 in enumerate(schedule):
        for op2 in schedule[i + 1:]:
            if are_conflicting(op1, op2):
                conflict_order.add((op1, op2))

    return conflict_order


def conflict_equivalent(schedule1, schedule2):
    # Compare the multiset of operations, ignoring their order.
    if sorted(schedule1) != sorted(schedule2):
        return False, "Schedules do not contain the same operations."

    conflicts1 = get_conflict_order(schedule1)
    conflicts2 = get_conflict_order(schedule2)

    if conflicts1 == conflicts2:
        return True, "Schedules are conflict-equivalent."

    return False, "Conflicting operation order differs."


def display_schedule(name, schedule):
    print(name)
    print(" -> ".join(
        f"T{t}:{action}({item})"
        for t, action, item in schedule
    ))


if __name__ == "__main__":
    schedule1 = [
        (1, "R", "A"),
        (1, "W", "A"),
        (2, "R", "A"),
        (2, "W", "A"),
    ]

    schedule2 = [
        (1, "R", "A"),
        (2, "R", "A"),
        (1, "W", "A"),
        (2, "W", "A"),
    ]

    display_schedule("Schedule 1:", schedule1)
    print()
    display_schedule("Schedule 2:", schedule2)

    equivalent, message = conflict_equivalent(
        schedule1, schedule2
    )

    print("\nConflict-equivalent:", equivalent)
    print("Result:", message)
