# Shared Lock Simulation


class SharedLock:
    def __init__(self):
        self.readers = 0

    def acquire(self, transaction):
        self.readers += 1
        print(transaction, "acquired Shared Lock")

    def release(self, transaction):
        self.readers -= 1
        print(transaction, "released Shared Lock")


lock = SharedLock()

lock.acquire("Transaction 1")
lock.acquire("Transaction 2")

print("Active Readers:", lock.readers)

lock.release("Transaction 1")
lock.release("Transaction 2")

print("Active Readers:", lock.readers)
