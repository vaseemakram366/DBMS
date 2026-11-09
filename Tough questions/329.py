# Two-Phase Locking (2PL) Protocol


class TwoPhaseLocking:
    def __init__(self):
        self.locks = {}
        self.phase = {}

    def acquire_lock(self, transaction, item):
        if self.phase.get(transaction) == "SHRINKING":
            print(f"{transaction}: Cannot acquire new lock!")
            return

        if item in self.locks and self.locks[item] != transaction:
            print(f"{transaction}: Lock unavailable for {item}")
            return

        self.locks[item] = transaction
        self.phase[transaction] = "GROWING"

        print(f"{transaction}: Lock acquired on {item}")

    def release_lock(self, transaction, item):
        if self.locks.get(item) == transaction:
            del self.locks[item]
            self.phase[transaction] = "SHRINKING"

            print(f"{transaction}: Lock released on {item}")


db = TwoPhaseLocking()

db.acquire_lock("T1", "A")
db.acquire_lock("T1", "B")

db.release_lock("T1", "A")

db.acquire_lock("T1", "C")
