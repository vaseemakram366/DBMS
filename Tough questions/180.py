# Transaction Schedule Recovery Graph Builder


from collections import defaultdict


def build_recovery_graph(schedule):
    last_writer = {}
    committed = set()
    commit_index = {}
    graph = defaultdict(set)
    dependencies = set()

    for index, (op, tid, item) in enumerate(schedule):
        if op == "C":
            committed.add(tid)
            commit_index[tid] = index

        elif op == "W":
            last_writer[item] = tid

        elif op == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != tid:
                graph[writer].add(tid)
                dependencies.add((writer, tid))

    violations = []

    for writer, reader in sorted(dependencies):
        if (
            writer in commit_index
            and reader in commit_index
            and commit_index[reader] < commit_index[writer]
        ):
            violations.append((writer, reader))

    return graph, violations


def display_graph(graph, violations):
    print("RECOVERY DEPENDENCY GRAPH")
    print("=" * 35)

    nodes = set(graph.keys())
    for targets in graph.values():
        nodes.update(targets)

    for node in sorted(nodes):
        targets = sorted(graph.get(node, set()))

        if targets:
            for target in targets:
                marker = "  [VIOLATION]" if (
                    node, target
                ) in violations else ""
                print(f"T{node} -> T{target}{marker}")
        else:
            print(f"T{node} -> (no outgoing edges)")

    print("=" * 35)
    print("Recovery violations:", violations)
    print("Recoverable:", not violations)


def main():
    schedule = [
        ("W", 1, "A"),
        ("R", 2, "A"),
        ("W", 2, "B"),
        ("C", 2, None),
        ("C", 1, None),
    ]

    graph, violations = build_recovery_graph(schedule)
    display_graph(graph, violations)


if __name__ == "__main__":
    main()
