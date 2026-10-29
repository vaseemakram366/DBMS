# Shared and Exclusive Lock Manager


class LockManager:
    def __init__(self):
        self.locks = {}

    def acquire(self, tid, item, mode):
        if mode not in ("S", "X"):
            print("Invalid lock mode")
            return False

        holders = self.locks.get(item, {})

        if tid in holders:
            current_mode = holders[tid]

            if current_mode == mode or current_mode == "X":
                print(f"{tid} already holds {current_mode} lock on {item}")
                return True

            if mode == "X" and len(holders) == 1:
                holders[tid] = "X"
                print(f"{tid} upgraded to X lock on {item}")
                return True

            print(f"{tid} cannot upgrade lock on {item}")
            return False

        if mode == "S":
            if any(lock == "X" for lock in holders.values()):
                print(f"{tid}: S lock denied on {item}")
                return False
        else:
            if holders:
                print(f"{tid}: X lock denied on {item}")
                return False

        holders[tid] = mode
        self.locks[item] = holders
        print(f"{tid} acquired {mode} lock on {item}")
        return True

    def release(self, tid, item):
        holders = self.locks.get(item, {})

        if tid not in holders:
            print(f"{tid} holds no lock on {item}")
            return False

        del holders[tid]

        if not holders:
            del self.locks[item]

        print(f"{tid} released lock on {item}")
        return True

    def show_locks(self):
        print("Current locks:", self.locks)


lm = LockManager()

lm.acquire("T1", "A", "S")
lm.acquire("T2", "A", "S")
lm.acquire("T3", "A", "X")

lm.release("T1", "A")
lm.release("T2", "A")

lm.acquire("T3", "A", "X")
lm.show_locks()
