# Exclusive Lock Simulation


class ExclusiveLock:
    def __init__(self):
        self.locked = False

    def acquire(self, transaction):
        if not self.locked:
            self.locked = True
            print(transaction, "acquired Exclusive Lock")
        else:
            print(transaction, "cannot acquire lock")

    def release(self, transaction):
        if self.locked:
            self.locked = False
            print(transaction, "released Exclusive Lock")


lock = ExclusiveLock()

lock.acquire("Transaction 1")
lock.acquire("Transaction 2")

lock.release("Transaction 1")

lock.acquire("Transaction 2")
lock.release("Transaction 2")
