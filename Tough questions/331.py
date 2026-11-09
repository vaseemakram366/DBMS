# Shared and Exclusive Locks


class LockManager:
    def __init__(self):
        self.shared_locks = {}
        self.exclusive_locks = {}

    def acquire_shared(self, transaction, item):
        owner = self.exclusive_locks.get(item)

        if owner is not None and owner != transaction:
            print(f"{transaction}: Shared lock denied on {item}")
            return

        self.shared_locks.setdefault(item, set()).add(transaction)
        print(f"{transaction}: Shared lock acquired on {item}")

    def acquire_exclusive(self, transaction, item):
        shared = self.shared_locks.get(item, set())
        exclusive = self.exclusive_locks.get(item)

        if (shared - {transaction}) or (
            exclusive is not None and exclusive != transaction
        ):
            print(f"{transaction}: Exclusive lock denied on {item}")
            return

        self.exclusive_locks[item] = transaction
        self.shared_locks.get(item, set()).discard(transaction)

        print(f"{transaction}: Exclusive lock acquired on {item}")


db = LockManager()

db.acquire_shared("T1", "A")
db.acquire_shared("T2", "A")

db.acquire_exclusive("T3", "A")
db.acquire_exclusive("T1", "A")
