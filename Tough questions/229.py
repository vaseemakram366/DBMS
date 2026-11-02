# Strict Two-Phase Locking (Strict 2PL)


class Strict2PL:
    def __init__(self, transaction):
        self.transaction = transaction
        self.locks = {}
        self.finished = False

    def acquire_lock(self, item, mode):
        if self.finished:
            print("Transaction already finished")
            return False

        if mode not in ("S", "X"):
            print("Invalid lock mode")
            return False

        current = self.locks.get(item)

        if current == "X" or current == mode:
            print(f"{mode} lock already held on {item}")
            return True

        if current == "S" and mode == "X":
            print(f"Cannot upgrade lock on {item} in this simulator")
            return False

        self.locks[item] = mode
        print(f"{self.transaction} acquired {mode} lock on {item}")
        return True

    def finish(self, action):
        if action not in ("COMMIT", "ABORT"):
            print("Invalid action")
            return

        if self.finished:
            print("Transaction already finished")
            return

        self.finished = True
        print(f"{self.transaction} {action}")

        for item in self.locks:
            print(f"Released {self.locks[item]} lock on {item}")

        self.locks.clear()


t1 = Strict2PL("T1")

t1.acquire_lock("Account", "X")
t1.acquire_lock("Balance", "S")
t1.finish("COMMIT")
    