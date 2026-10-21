# Lock Wait Queue Manager


from collections import defaultdict, deque


class LockWaitQueueManager:
    def __init__(self):
        self.lock_table = defaultdict(dict)
        self.wait_queues = defaultdict(deque)
        self.held_locks = defaultdict(dict)

    def acquire_lock(self, tx, resource, mode):
        if mode not in ("S", "X"):
            print("Invalid lock mode")
            return

        holders = self.lock_table[resource]

        # Already holds a lock on this resource
        if tx in holders:
            current = holders[tx]

            if current == "X" or current == mode:
                print(f"{tx} already holds {current} lock")
                return

            if current == "S" and mode == "X":
                others = {
                    owner: lock
                    for owner, lock in holders.items()
                    if owner != tx
                }

                if not others and not self.wait_queues[resource]:
                    holders[tx] = "X"
                    self.held_locks[tx][resource] = "X"
                    print(f"{tx} upgraded to X on {resource}")
                    return

                print(f"{tx} queued for X upgrade on {resource}")
                self.wait_queues[resource].append((tx, mode))
                return

        # Keep queue order to prevent bypassing earlier requests
        if self.wait_queues[resource]:
            self.wait_queues[resource].append((tx, mode))
            print(f"{tx} waiting for {mode} on {resource}")
            return

        compatible = all(
            mode == "S" and held_mode == "S"
            for owner, held_mode in holders.items()
            if owner != tx
        )

        if compatible:
            holders[tx] = mode
            self.held_locks[tx][resource] = mode
            print(f"{tx} acquired {mode} on {resource}")
        else:
            self.wait_queues[resource].append((tx, mode))
            print(f"{tx} waiting for {mode} on {resource}")

    def _grant_waiters(self, resource):
        queue = self.wait_queues[resource]
        holders = self.lock_table[resource]

        while queue:
            tx, mode = queue[0]

            # Don't grant a lock to a transaction already holding it.
            if tx in holders:
                queue.popleft()
                continue

            # Only compatible requests at the front may proceed.
            if mode == "X" and holders:
                break

            if mode == "S" and any(
                held_mode == "X" for held_mode in holders.values()
            ):
                break

            queue.popleft()
            holders[tx] = mode
            self.held_locks[tx][resource] = mode
            print(f"{tx} granted {mode} on {resource}")

            # Grant a shared-lock batch, but stop after an exclusive lock.
            if mode == "X":
                break

            if queue and queue[0][1] == "X":
                break

        if not queue:
            self.wait_queues.pop(resource, None)

    def release_lock(self, tx, resource):
        if resource not in self.held_locks.get(tx, {}):
            print(f"{tx} holds no lock on {resource}")
            return

        del self.held_locks[tx][resource]
        del self.lock_table[resource][tx]

        if not self.lock_table[resource]:
            del self.lock_table[resource]

        print(f"{tx} released lock on {resource}")
        self._grant_waiters(resource)

        if not self.held_locks[tx]:
            del self.held_locks[tx]

    def show_wait_queue(self, resource):
        queue = self.wait_queues.get(resource, deque())
        print(f"Wait queue for {resource}: {list(queue)}")


# Demonstration
db = LockWaitQueueManager()

db.acquire_lock("T1", "Account-A", "X")
db.acquire_lock("T2", "Account-A", "X")
db.acquire_lock("T3", "Account-A", "S")

db.show_wait_queue("Account-A")

db.release_lock("T1", "Account-A")
db.show_wait_queue("Account-A")

db.release_lock("T2", "Account-A")
db.show_wait_queue("Account-A")

db.release_lock("T3", "Account-A")
