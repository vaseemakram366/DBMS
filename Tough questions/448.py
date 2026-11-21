# Strict Two-Phase Locking (Strict 2PL) Simulation


class Transaction:
    def __init__(self):
        self.locks = []

    def acquire_lock(self, resource):
        self.locks.append(resource)
        print("Lock acquired:", resource)

    def commit(self):
        print("Transaction committed")

        for resource in self.locks:
            print("Lock released:", resource)

        self.locks.clear()


t1 = Transaction()

t1.acquire_lock("Account A")
t1.acquire_lock("Account B")

print("Locks held:", t1.locks)

t1.commit()

print("Locks held after commit:", t1.locks)
