# Transaction Recovery Cycle Detector


from collections import defaultdict


def build_graph(schedule):
    last_writer = {}
    graph = defaultdict(set)
    transactions = set()

    for op, tid, item in schedule:
        transactions.add(tid)

        if op == "W":
            last_writer[item] = tid

        elif op == "R":
            writer = last_writer.get(item)

            if writer is not None and writer != tid:
                graph[writer].add(tid)

    for tid in transactions:
        graph[tid]  # Ensure every transaction is represented.

    return graph, transactions


def find_cycle(graph, transactions):
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {tid: WHITE for tid in transactions}
    parent = {}
    cycle = []

    def dfs(node):
        nonlocal cycle
        color[node] = GRAY

        for neighbor in sorted(graph[node]):
            if color[neighbor] == WHITE:
                parent[neighbor] = node

                if dfs(neighbor):
                    return True

            elif color[neighbor] == GRAY:
                # A back edge identifies a cycle.
                path = [node]
                current = node

                while current != neighbor:
                    current = parent[current]
                    path.append(current)

                path.reverse()
                path.append(neighbor)
                cycle = path
                return True

        color[node] = BLACK
        return False

    for tid in sorted(transactions):
        if color[tid] == WHITE and dfs(tid):
            return cycle

    return None


def main():
    schedule = [
        ("W", 1, "A"),
        ("R", 2, "A"),  # T1 -> T2
        ("W", 2, "B"),
        ("R", 3, "B"),  # T2 -> T3
        ("W", 3, "C"),
        ("R", 1, "C"),  # T3 -> T1
    ]

    graph, transactions = build_graph(schedule)

    print("Recovery dependency graph:")
    for tid in sorted(transactions):
        for neighbor in sorted(graph[tid]):
            print(f"T{tid} -> T{neighbor}")

    cycle = find_cycle(graph, transactions)

    if cycle:
        print("\nCycle detected:")
        print(" -> ".join(f"T{tid}" for tid in cycle))
        print("A topological recovery order is impossible.")
    else:
        print("\nNo cycle detected.")
        print("A topological recovery order exists.")


if __name__ == "__main__":
    main()
