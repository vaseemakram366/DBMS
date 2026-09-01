# Two-Phase Locking (2PL) Simulator

class LockManager:
    def __init__(self):
        self.locks = {}

    def acquire(self, transaction, item, lock_type):
        if item not in self.locks:
            self.locks[item] = []

        current = self.locks[item]

        if lock_type == "S":
            if all(t == transaction or l == "S"
                   for t, l in current):
                current.append((transaction, "S"))
                print(transaction, "acquired Shared Lock on", item)
                return True

        elif lock_type == "X":
            if len(current) == 0 or (
                len(current) == 1 and current[0][0] == transaction
            ):
                self.locks[item] = [(transaction, "X")]
                print(transaction, "acquired Exclusive Lock on", item)
                return True

        print(transaction, "blocked on", item)
        return False

    def release(self, transaction, item):
        if item in self.locks:
            self.locks[item] = [
                (t, l) for t, l in self.locks[item]
                if t != transaction
            ]

            print(transaction, "released lock on", item)


lm = LockManager()

lm.acquire("T1", "A", "S")
lm.acquire("T2", "A", "S")
lm.acquire("T3", "A", "X")

lm.release("T1", "A")
lm.release("T2", "A")

lm.acquire("T3", "A", "X")