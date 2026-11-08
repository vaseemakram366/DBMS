# Lock Timeout Simulator


class LockTimeout:
    def __init__(self, timeout):
        self.timeout = timeout
        self.locks = {}

    def acquire_lock(self, transaction, item, wait_time):
        if item not in self.locks:
            self.locks[item] = transaction
            print(f"{transaction}: Lock GRANTED on {item}")
            return

        if self.locks[item] == transaction:
            print(f"{transaction}: Lock already held on {item}")
            return

        print(f"{transaction}: Waiting for {item}")

        if wait_time >= self.timeout:
            print(f"{transaction}: TIMEOUT - ABORT")
        else:
            print(f"{transaction}: Still WAITING")

    def release_lock(self, transaction, item):
        if self.locks.get(item) == transaction:
            del self.locks[item]
            print(f"{transaction}: Lock released on {item}")


db = LockTimeout(timeout=5)

db.acquire_lock("T1", "A", 0)
db.acquire_lock("T2", "A", 3)
db.acquire_lock("T3", "A", 5)

db.release_lock("T1", "A")
db.acquire_lock("T2", "A", 0)
