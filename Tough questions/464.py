# Topological Sorting of Transactions


graph = {
    "T1": ["T2"],
    "T2": ["T3"],
    "T3": []
}

visited = set()
stack = []

def topological_sort(node):
    visited.add(node)

    for neighbor in graph[node]:
        if neighbor not in visited:
            topological_sort(neighbor)

    stack.append(node)


for transaction in graph:
    if transaction not in visited:
        topological_sort(transaction)

order = stack[::-1]

print("Topological Order:")

for transaction in order:
    print(transaction, end=" ")

print()
