# Two-Phase Locking (2PL) Protocol Simulator


class TwoPhaseLocking:
    def __init__(self):
        self.locks = {}
        self.transaction_locks = {}
        self.phase = {}

    def begin(self, tid):
        self.transaction_locks[tid] = set()
        self.phase[tid] = "GROWING"
        print(f"{tid} started in GROWING phase")

    def acquire_lock(self, tid, item):
        if tid not in self.phase:
            print(f"{tid}: transaction not found")
            return False

        if self.phase[tid] == "SHRINKING":
            print(f"{tid}: lock denied; transaction is SHRINKING")
            return False

        owner = self.locks.get(item)

        if owner is not None and owner != tid:
            print(f"{tid}: lock denied on {item}; held by {owner}")
            return False

        self.locks[item] = tid
        self.transaction_locks[tid].add(item)
        print(f"{tid} acquired lock on {item}")
        return True

    def release_lock(self, tid, item):
        if item not in self.transaction_locks.get(tid, set()):
            print(f"{tid}: does not hold lock on {item}")
            return False

        del self.locks[item]
        self.transaction_locks[tid].remove(item)
        self.phase[tid] = "SHRINKING"

        print(f"{tid} released lock on {item}")
        print(f"{tid} entered SHRINKING phase")
        return True

    def show_locks(self):
        print("Current locks:", self.locks)


db = TwoPhaseLocking()

db.begin("T1")
db.acquire_lock("T1", "A")
db.acquire_lock("T1", "B")

db.release_lock("T1", "A")
db.acquire_lock("T1", "C")

db.show_locks()
