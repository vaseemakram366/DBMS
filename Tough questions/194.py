# Lock Upgrade and Downgrade Simulator


class LockUpgradeDowngrade:
    def __init__(self):
        self.locks = {}

    def acquire(self, tid, item, mode):
        holders = self.locks.setdefault(item, {})

        if mode == "S":
            if any(
                owner != tid and lock == "X"
                for owner, lock in holders.items()
            ):
                print(f"{tid}: S lock denied on {item}")
                return False

        elif mode == "X":
            if any(owner != tid for owner in holders):
                print(f"{tid}: X lock denied on {item}")
                return False
        else:
            print("Invalid lock mode")
            return False

        holders[tid] = mode
        print(f"{tid} acquired {mode} lock on {item}")
        return True

    def upgrade(self, tid, item):
        holders = self.locks.get(item, {})

        if holders.get(tid) != "S":
            print(f"{tid}: cannot upgrade; no S lock on {item}")
            return False

        if any(owner != tid for owner in holders):
            print(f"{tid}: upgrade denied; other locks exist on {item}")
            return False

        holders[tid] = "X"
        print(f"{tid} upgraded S -> X on {item}")
        return True

    def downgrade(self, tid, item):
        holders = self.locks.get(item, {})

        if holders.get(tid) != "X":
            print(f"{tid}: cannot downgrade; no X lock on {item}")
            return False

        holders[tid] = "S"
        print(f"{tid} downgraded X -> S on {item}")
        return True

    def show_locks(self):
        print("Current locks:", self.locks)


lm = LockUpgradeDowngrade()

lm.acquire("T1", "A", "S")
lm.acquire("T2", "A", "S")

lm.upgrade("T1", "A")

lm.release = None
