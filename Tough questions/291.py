# Shared and Exclusive Locking


class SharedExclusiveLock:
    def __init__(self):
        self.shared_locks = []
        self.exclusive_lock = None

    def acquire_shared(self, transaction):
        if self.exclusive_lock is None:
            self.shared_locks.append(transaction)
            print(transaction, "acquired Shared Lock")
        else:
            print(transaction, "cannot acquire Shared Lock")

    def acquire_exclusive(self, transaction):
        if self.exclusive_lock is None and not self.shared_locks:
            self.exclusive_lock = transaction
            print(transaction, "acquired Exclusive Lock")
        else:
            print(transaction, "cannot acquire Exclusive Lock")

    def release_shared(self, transaction):
        if transaction in self.shared_locks:
            self.shared_locks.remove(transaction)
            print(transaction, "released Shared Lock")

    def release_exclusive(self, transaction):
        if self.exclusive_lock == transaction:
            self.exclusive_lock = None
            print(transaction, "released Exclusive Lock")


db = SharedExclusiveLock()

db.acquire_shared("T1")
db.acquire_shared("T2")

db.acquire_exclusive("T3")

db.release_shared("T1")
db.release_shared("T2")

db.acquire_exclusive("T3")
