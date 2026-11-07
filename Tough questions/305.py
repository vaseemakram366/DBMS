# Two-Phase Locking (2PL) Simulator


class TwoPhaseLocking:
    def __init__(self):
        self.phase = "GROWING"
        self.locks = set()

    def acquire_lock(self, item):
        if self.phase == "SHRINKING":
            print(
                f"Cannot acquire {item}: "
                "Growing phase has ended"
            )
            return

        self.locks.add(item)
        print(f"Lock acquired on {item}")

    def release_lock(self, item):
        if item in self.locks:
            self.locks.remove(item)
            self.phase = "SHRINKING"
            print(f"Lock released on {item}")
        else:
            print(f"No lock held on {item}")

    def show_status(self):
        print("Current Phase:", self.phase)
        print("Held Locks:", sorted(self.locks))


db = TwoPhaseLocking()

db.acquire_lock("A")
db.acquire_lock("B")

db.release_lock("A")

db.acquire_lock("C")

db.show_status()
