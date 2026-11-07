# Shared and Exclusive Lock Manager


class LockManager:
    def __init__(self):
        self.locks = {}

    def acquire_lock(self, transaction, item, lock_type):
        current = self.locks.get(item, [])

        if lock_type == "S":
            if any(mode == "X" and tx != transaction
                   for tx, mode in current):
                print(f"{transaction}: Shared lock DENIED on {item}")
                return

        elif lock_type == "X":
            if any(tx != transaction for tx, mode in current):
                print(f"{transaction}: Exclusive lock DENIED on {item}")
                return

        self.locks.setdefault(item, [])

        existing = [
            mode for tx, mode in self.locks[item]
            if tx == transaction
        ]

        if lock_type == "X" and "X" in existing:
            print(f"{transaction}: Already holds X lock on {item}")
            return

        if lock_type == "S" and ("S" in existing or "X" in existing):
            print(f"{transaction}: Lock already held on {item}")
            return

        self.locks[item].append((transaction, lock_type))
        print(f"{transaction}: {lock_type} lock GRANTED on {item}")


db = LockManager()

db.acquire_lock("T1", "A", "S")
db.acquire_lock("T2", "A", "S")
db.acquire_lock("T3", "A", "X")
