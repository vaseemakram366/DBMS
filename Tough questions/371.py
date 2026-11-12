# Buffer Hit and Miss Ratio


from collections import deque

capacity = 3
requests = [1, 2, 1, 3, 2, 4]

buffer = set()
queue = deque()

hits = 0
misses = 0

for page in requests:
    if page in buffer:
        hits += 1
        print(f"Page {page}: Hit")
    else:
        misses += 1
        print(f"Page {page}: Miss")

        if len(queue) == capacity:
            removed = queue.popleft()
            buffer.remove(removed)
            print("Removed page:", removed)

        queue.append(page)
        buffer.add(page)

total = len(requests)

print("Total accesses:", total)
print("Hits:", hits)
print("Misses:", misses)
print(f"Hit ratio: {hits / total:.2f}")
print(f"Miss ratio: {misses / total:.2f}")
