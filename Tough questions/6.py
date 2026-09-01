# Conflict Serializability Checker

def conflict_serializable(schedule):
    graph = {}
    transactions = set()

    # Create transaction set
    for transaction, operation, item in schedule:
        transactions.add(transaction)
        graph[transaction] = []

    # Build precedence graph
    for i in range(len(schedule)):
        t1, op1, item1 = schedule[i]

        for j in range(i + 1, len(schedule)):
            t2, op2, item2 = schedule[j]

            # Different transactions
            if t1 != t2 and item1 == item2:

                # At least one operation must be WRITE
                if op1 == "W" or op2 == "W":
                    if t2 not in graph[t1]:
                        graph[t1].append(t2)

    # DFS cycle detection
    visited = set()
    recursion_stack = set()

    def dfs(node):
        visited.add(node)
        recursion_stack.add(node)

        for neighbour in graph[node]:

            if neighbour not in visited:
                if dfs(neighbour):
                    return True

            elif neighbour in recursion_stack:
                return True

        recursion_stack.remove(node)
        return False

    # Check cycle
    for transaction in transactions:
        if transaction not in visited:
            if dfs(transaction):
                return False, graph

    return True, graph


schedule = [
    ("T1", "R", "A"),
    ("T2", "R", "B"),
    ("T1", "W", "B"),
    ("T2", "W", "A")
]

result, graph = conflict_serializable(schedule)

print("Precedence Graph:")
for t in graph:
    print(t, "->", graph[t])

if result:
    print("\nSchedule is Conflict Serializable")
else:
    print("\nSchedule is NOT Conflict Serializable")