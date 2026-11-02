# Database Lock Manager


class LockManager:
    def __init__(self):
        self.locks = {}

    def acquire(self, transaction, item, mode):
        if mode not in ("S", "X"):
            print("Invalid lock mode")
            return False

        holders = self.locks.setdefault(item, {})

        if transaction in holders:
            current_mode = holders[transaction]

            if current_mode == "X" or current_mode == mode:
                print(f"{transaction} already holds {current_mode} lock on {item}")
                return True

            if mode == "X" and len(holders) == 1:
                holders[transaction] = "X"
                print(f"{transaction} upgraded to X lock on {item}")
                return True

        if mode == "S":
            if all(lock_mode == "S" for lock_mode in holders.values()):
                holders[transaction] = "S"
                print(f"{transaction} acquired S lock on {item}")
                return True
        else:
            if not holders:
                holders[transaction] = "X"
                print(f"{transaction} acquired X lock on {item}")
                return True

        print(f"{transaction} denied {mode} lock on {item}")
        return False

    def release(self, transaction, item):
        holders = self.locks.get(item, {})

        if transaction in holders:
            del holders[transaction]
            print(f"{transaction} released lock on {item}")

            if not holders:
                del self.locks[item]
        else:
            print(f"{transaction} has no lock on {item}")


manager = LockManager()

manager.acquire("T1", "Account", "S")
manager.acquire("T2", "Account", "S")
manager.acquire("T3", "Account", "X")

manager.release("T1", "Account")
manager.release("T2", "Account")

manager.acquire("T3", "Account", "X")
