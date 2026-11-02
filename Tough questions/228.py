# Two-Phase Locking (2PL) Simulator


class TwoPhaseLocking:
    def __init__(self):
        self.locks = set()
        self.phase = "GROWING"

    def acquire_lock(self, item):
        if self.phase == "SHRINKING":
            print(f"Cannot acquire {item}: shrinking phase")
            return False

        self.locks.add(item)
        print(f"Lock acquired: {item}")
        return True

    def release_lock(self, item):
        if item in self.locks:
            self.locks.remove(item)
            self.phase = "SHRINKING"
            print(f"Lock released: {item}")
        else:
            print(f"No lock held on: {item}")

    def show_status(self):
        print("Current phase:", self.phase)
        print("Active locks:", sorted(self.locks))


t1 = TwoPhaseLocking()

t1.acquire_lock("Account")
t1.acquire_lock("Balance")
t1.release_lock("Account")
t1.acquire_lock("Customer")
t1.show_status()
