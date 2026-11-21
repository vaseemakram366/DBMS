# Two-Phase Locking (2PL) Simulation


class Transaction:
    def __init__(self):
        self.locks = []
        self.growing = True

    def acquire_lock(self, resource):
        if self.growing:
            self.locks.append(resource)
            print("Lock acquired:", resource)
        else:
            print("Cannot acquire lock during shrinking phase")

    def release_lock(self, resource):
        if resource in self.locks:
            self.locks.remove(resource)
            self.growing = False
            print("Lock released:", resource)


t1 = Transaction()

print("Growing Phase:")
t1.acquire_lock("Resource A")
t1.acquire_lock("Resource B")

print("\nShrinking Phase:")
t1.release_lock("Resource A")
t1.acquire_lock("Resource C")
t1.release_lock("Resource B")
