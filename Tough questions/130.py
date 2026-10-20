# Database Lock Timeout Manager


from threading import Lock
from time import perf_counter, sleep


class LockTimeoutManager:

    def __init__(self):
        self.resource_locks = {}

    def get_lock(self, resource):
        if resource not in self.resource_locks:
            self.resource_locks[resource] = Lock()

        return self.resource_locks[resource]

    def acquire_lock(self, tx_id, resource, timeout_seconds=3):
        lock = self.get_lock(resource)

        print(f"{tx_id} requesting lock on {resource}...")

        start = perf_counter()
        acquired = lock.acquire(timeout=timeout_seconds)
        elapsed = perf_counter() - start

        if acquired:
            print(
                f"SUCCESS: {tx_id} acquired lock "
                f"after {elapsed:.2f} seconds."
            )
            return lock

        print(
            f"TIMEOUT: {tx_id} could not acquire lock "
            f"within {timeout_seconds} seconds."
        )
        return None

    def release_lock(self, tx_id, lock):
        if lock is not None:
            lock.release()
            print(f"{tx_id} released the lock.")


manager = LockTimeoutManager()

# T1 acquires the lock first.
lock_t1 = manager.acquire_lock("T1", "Account-A")

# T2 waits, but times out after one second.
lock_t2 = manager.acquire_lock(
    "T2",
    "Account-A",
    timeout_seconds=1
)

manager.release_lock("T1", lock_t1)

# T2 retries after T1 releases the lock.
lock_t2 = manager.acquire_lock(
    "T2",
    "Account-A",
    timeout_seconds=1
)

manager.release_lock("T2", lock_t2)
