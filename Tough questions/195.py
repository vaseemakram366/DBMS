# Lock Wait Queue Simulator


from collections import deque


class LockWaitQueue:
    def __init__(self):
        self.locks = {}
        self.waiting = {}
        self.transaction_locks = {}

    def acquire(self, tid, item, mode):
        if mode not in ("S", "X"):
            print("Invalid lock mode")
            return False

        holders = self.locks.get(item, {})
        queue = self.waiting.setdefault(item, deque())

        if tid in holders:
            print(f"{tid} already holds a lock on {item}")
            return False

        if any(request[0] == tid for request in queue):
            print(f"{tid} is already waiting for {item}")
            return False

        compatible = (
            mode == "S"
            and all(lock == "S" for lock in holders.values())
            and not queue
        )

        if not holders and not queue:
            compatible = True

        if compatible:
            holders[tid] = mode
            self.locks[item] = holders
            self.transaction_locks.setdefault(tid, set()).add(item)
            print(f"{tid} granted {mode} lock on {item}")
            return True

        queue.append((tid, mode))
        print(f"{tid} queued for {mode} lock on {item}")
        return False

    def release(self, tid, item):
        holders = self.locks.get(item, {})

        if tid not in holders:
            print(f"{tid} holds no lock on {item}")
            return False

        del holders[tid]
        self.transaction_locks[tid].discard(item)

        if not holders:
            self.locks.pop(item, None)

        print(f"{tid} released lock on {item}")
        self.grant_waiters(item)
        return True

    def grant_waiters(self, item):
        queue = self.waiting.setdefault(item, deque())
        holders = self.locks.setdefault(item, {})

        if not queue:
            self.waiting.pop(item, None)
            self.locks.pop(item, None)
            return

        # Grant one exclusive request or a consecutive
        # group of shared requests at the front.
        if holders:
            return

        first_tid, first_mode = queue.popleft()
        holders[first_tid] = first_mode
        self.transaction_locks.setdefault(first_tid, set()).add(item)
        print(f"{first_tid} granted {first_mode} lock on {item}")

        if first_mode == "S":
            while queue and queue[0][1] == "S":
                tid, mode = queue.popleft()
                holders[tid] = mode
                self.transaction_locks.setdefault(tid, set()).add(item)
                print(f"{tid} granted {mode} lock on {item}")

        if not queue:
            self.waiting.pop(item, None)

    def show_state(self, item):
        print("Locks:", self.locks.get(item, {}))
        print("Waiting:", list(self.waiting.get(item, [])))


lm = LockWaitQueue()

lm.acquire("T1", "A", "X")
lm.acquire("T2", "A", "S")
lm.acquire("T3", "A", "S")

lm.show_state("A")

lm.release("T1", "A")
lm.show_state("A")
