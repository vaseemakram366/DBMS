# Two-Phase Locking (2PL)


class TwoPhaseLocking:
    def __init__(self):
        self.locks = set()
        self.phase = "GROWING"

    def acquire_lock(self, resource):
        if self.phase == "GROWING":
            self.locks.add(resource)
            print("Lock acquired:", resource)
        else:
            print("Cannot acquire lock in shrinking phase")

    def release_lock(self, resource):
        if resource in self.locks:
            self.locks.remove(resource)
            self.phase = "SHRINKING"
            print("Lock released:", resource)

    def display(self):
        print("Current Phase:", self.phase)
        print("Active Locks:", self.locks)


db = TwoPhaseLocking()

db.acquire_lock("Account")
db.acquire_lock("Database")

db.display()

db.release_lock("Account")

db.acquire_lock("Employee")

db.display()
