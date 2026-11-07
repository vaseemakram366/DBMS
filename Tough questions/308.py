# Multiple Granularity Locking


class MultipleGranularityLocking:
    def __init__(self):
        self.locks = {}

    def acquire_lock(self, transaction, item, lock_type):
        self.locks.setdefault(item, [])

        current = self.locks[item]

        if lock_type == "S":
            if any(mode in ("X", "IX") and tx != transaction
                   for tx, mode in current):
                print(f"{transaction}: S Lock DENIED on {item}")
                return

        elif lock_type == "X":
            if any(tx != transaction for tx, mode in current):
                print(f"{transaction}: X Lock DENIED on {item}")
                return

        self.locks[item].append((transaction, lock_type))
        print(f"{transaction}: {lock_type} Lock GRANTED on {item}")


db = MultipleGranularityLocking()

db.acquire_lock("T1", "Database", "IX")
db.acquire_lock("T1", "TableA", "IX")
db.acquire_lock("T1", "Record1", "X")

db.acquire_lock("T2", "Database", "IS")
db.acquire_lock("T2", "TableA", "S")
