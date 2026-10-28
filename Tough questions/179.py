# Transaction Schedule Recovery Visualizer


def visualize_recovery(schedule):
    last_writer = {}
    committed = set()
    commit_index = {}
    dependencies = set()
    dirty_reads = []

    print("TRANSACTION RECOVERY TIMELINE")
    print("=" * 55)

    for index, (op, tid, item) in enumerate(schedule):
        if op == "W":
            print(f"{index:02d} | T{tid} WRITE  {item}")
            last_writer[item] = tid

        elif op == "R":
            writer = last_writer.get(item)

            if writer is None or writer == tid:
                print(f"{index:02d} | T{tid} READ   {item}")
            else:
                dependencies.add((writer, tid))

                if writer not in committed:
                    dirty_reads.append((tid, writer, item))
                    print(
                        f"{index:02d} | T{tid} READ   {item} "
                        f"<-- DIRTY READ from T{writer}"
                    )
                else:
                    print(
                        f"{index:02d} | T{tid} READ   {item} "
                        f"<-- committed value from T{writer}"
                    )

        elif op == "C":
            committed.add(tid)
            commit_index[tid] = index
            print(f"{index:02d} | T{tid} COMMIT")

    violations = [
        (writer, reader)
        for writer, reader in dependencies
        if (
            writer in commit_index
            and reader in commit_index
            and commit_index[reader] < commit_index[writer]
        )
    ]

    recoverable = not violations
    cascadeless = not dirty_reads

    print("=" * 55)
    print("Dirty reads:", len(dirty_reads))
    print("Recovery violations:", violations)
    print("Recoverable:", recoverable)
    print("Cascadeless:", cascadeless)


def main():
    schedule = [
        ("W", 1, "A"),
        ("R", 2, "A"),
        ("W", 2, "B"),
        ("C", 2, None),
        ("C", 1, None),
    ]

    visualize_recovery(schedule)


if __name__ == "__main__":
    main()
