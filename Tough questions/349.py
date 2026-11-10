# Deadlock Detection with Multiple Transactions


from collections import deque

def detect_deadlock(graph):
    indegree = {tx: 0 for tx in graph}

    for tx in graph:
        for neighbor in graph[tx]:
            indegree[neighbor] += 1

    queue = deque()

    for tx in indegree:
        if indegree[tx] == 0:
            queue.append(tx)

    count = 0

    while queue:
        tx = queue.popleft()
        count += 1

        for neighbor in graph[tx]:
            indegree[neighbor] -= 1

            if indegree[neighbor] == 0:
                queue.append(neighbor)

    if count != len(graph):
        print("Deadlock detected!")
    else:
        print("No deadlock detected.")


graph = {
    "T1": ["T2"],
    "T2": ["T3"],
    "T3": ["T4"],
    "T4": ["T2"],
    "T5": []
}

detect_deadlock(graph)
