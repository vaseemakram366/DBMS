# Strict Two-Phase Locking (Strict 2PL)


class Strict2PL:
    def __init__(self):
        self.locks = {}

    def acquire_lock(self, transaction, item):
        if item in self.locks and self.locks[item] != transaction:
            print(f"{transaction}: Lock unavailable on {item}")
            return False

        self.locks[item] = transaction
        print(f"{transaction}: Lock acquired on {item}")
        return True

    def release_all(self, transaction):
        released = []

        for item, owner in list(self.locks.items()):
            if owner == transaction:
                released.append(item)
                del self.locks[item]

        print(f"{transaction}: Released locks {released}")

    def commit(self, transaction):
        print(f"{transaction}: COMMIT")
        self.release_all(transaction)


db = Strict2PL()

db.acquire_lock("T1", "A")
db.acquire_lock("T2", "A")

db.commit("T1")

db.acquire_lock("T2", "A")
db.commit("T2")
