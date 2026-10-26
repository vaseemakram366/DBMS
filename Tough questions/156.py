Transaction Schedule Mutation Tester/


import random


def check_recoverability(schedule):
    last_writer = {}
    dependencies = []
    commit_order = {}

    for index, (tx, op, item) in enumerate(schedule):
        if op == "W":
            last_writer[item] = tx

        elif op == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != tx:
                dependencies.append((writer, tx))

        elif op == "C":
            commit_order[tx] = index

    for writer, reader in dependencies:
        if reader in commit_order:
            if (
                writer not in commit_order
                or commit_order[writer] > commit_order[reader]
            ):
                return False

    return True


def mutate_commit_order(schedule):
    mutated = schedule.copy()

    commit_positions = {
        tx: i
        for i, (tx, op, _) in enumerate(mutated)
        if op == "C"
    }

    # Find a writer-reader dependency.
    last_writer = {}
    dependency = None

    for tx, op, item in mutated:
        if op == "W":
            last_writer[item] = tx
        elif op == "R":
            writer = last_writer.get(item)
            if writer is not None and writer != tx:
                dependency = (writer, tx)
                break

    if dependency is None:
        return None

    writer, reader = dependency

    if writer not in commit_positions or reader not in commit_positions:
        return None

    # Swap commit operations to reverse their order.
    i = commit_positions[writer]
    j = commit_positions[reader]

    mutated[i], mutated[j] = mutated[j], mutated[i]

    return mutated


def show_schedule(schedule):
    for tx, op, item in schedule:
        if op in ("R", "W"):
            print(f"{tx}: {op}({item})")
        else:
            print(f"{tx}: COMMIT")


original = [
    ("T1", "W", "A"),
    ("T1", "C", ""),
    ("T2", "R", "A"),
    ("T2", "C", ""),
]

print("Original Schedule:")
show_schedule(original)
print("Recoverable:", check_recoverability(original))

mutated = [
    ("T1", "W", "A"),
    ("T2", "R", "A"),
    ("T2", "C", ""),
    ("T1", "C", ""),
]

print("\nMutated Schedule:")
show_schedule(mutated)
print("Recoverable:", check_recoverability(mutated))
