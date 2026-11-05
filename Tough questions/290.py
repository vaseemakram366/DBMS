# Strict Two-Phase Locking (Strict 2PL)


class StrictTwoPhaseLocking:
    def __init__(self):
        self.locks = set()
        self.active = True

    def acquire_lock(self, resource):
        if self.active:
            self.locks.add(resource)
            print("Lock acquired:", resource)

    def commit(self):
        print("\nTransaction committed")

        self.active = False
        self.locks.clear()

        print("All locks released")

    def display_locks(self):
        print("Active Locks:", self.locks)


db = StrictTwoPhaseLocking()

db.acquire_lock("Account")
db.acquire_lock("Employee")

db.display_locks()

db.commit()

db.display_locks()
