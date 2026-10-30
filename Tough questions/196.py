# Database Lock Table and Deadlock Integration Simulator


from collections import deque


class DatabaseLockManager:
    def __init__(self):
        self.lock_table = {}
        self.wait_queues = {}
        self.waiting_for = {}
        self.held_locks = {}

    def acquire(self, tid, item, mode):
        if mode not in ("S", "X"):
            print("Invalid lock mode")
            return False

        holders = self.lock_table.get(item, {})
        queue = self.wait_queues.setdefault(item, deque())

        if tid in holders:
            print(f"{tid} already holds a lock on {item}")
            return False

        if any(waiter == tid for waiter, _ in queue):
            print(f"{tid} is already waiting for {item}")
            return False

        conflicts = [
            owner for owner, held_mode in holders.items()
            if owner != tid and (mode == "X" or held_mode == "X")
        ]

        # Prevent bypassing earlier queued requests.
        if conflicts or queue:
            queue.append((tid, mode))
            self.waiting_for[tid] = set(conflicts)
            print(f"{tid} waits for {item}")

            if not conflicts:
                # The earlier queued request is the blocker.
                self.waiting_for[tid].add(queue[-2][0])

            return False

        self.lock_table.setdefault(item, {})[tid] = mode
        self.held_locks.setdefault(tid, set()).add(item)
        print(f"{tid} acquired {mode} lock on {item}")
        return True

    def release(self, tid, item):
        holders = self.lock_table.get(item, {})

        if tid not in holders:
            print(f"{tid} holds no lock on {item}")
            return False

        del holders[tid]
        self.held_locks.get(tid, set()).discard(item)
        print(f"{tid} released lock on {item}")

        if not holders:
            self.lock_table.pop(item, None)

        self._process_queue(item)
        return True

    def _process_queue(self, item):
        queue = self.wait_queues.get(item)
        if not queue:
            return

        holders = self.lock_table.get(item, {})

        while queue:
            tid, mode = queue[0]

            conflicts = any(
                owner != tid and (mode == "X" or held_mode == "X")
                for owner, held_mode in holders.items()
            )

            if conflicts:
                break

            # Grant only compatible requests at the queue front.
            queue.popleft()
            holders[tid] = mode
            self.held_locks.setdefault(tid, set()).add(item)
            self.waiting_for.pop(tid, None)
            print(f"{tid} granted {mode} lock on {item}")

            if mode == "X":
                break

        if not queue:
            self.wait_queues.pop(item, None)

        if not holders:
            self.lock_table.pop(item, None)

    def detect_deadlock(self):
        graph = {
            tid: set(blockers)
            for tid, blockers in self.waiting_for.items()
        }

        visited = set()
        active = set()
        path = []

        def dfs(node):
            visited.add(node)
            active.add(node)
            path.append(node)

            for neighbor in graph.get(node, set()):
                if neighbor not in visited:
                    cycle = dfs(neighbor)
                    if cycle:
                        return cycle
                elif neighbor in active:
                    index = path.index(neighbor)
                    return path[index:] + [neighbor]

            path.pop()
            active.remove(node)
            return None

        for node in graph:
            if node not in visited:
                cycle = dfs(node)
                if cycle:
                    print("Deadlock detected:", " -> ".join(cycle))
                    return True

        print("No deadlock detected")
        return False

    def show_lock_table(self):
        print("Lock table:", self.lock_table)


db = DatabaseLockManager()

db.acquire("T1", "A", "X")
db.acquire("T2", "B", "X")

db.acquire("T1", "B", "X")
db.acquire("T2", "A", "X")

db.show_lock_table()
db.detect_deadlock()
