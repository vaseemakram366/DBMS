# Lock Manager with Multiple Transactions


class LockManager:
    def __init__(self):
        self.shared = {}
        self.exclusive = {}

    def acquire_shared(self, tx, item):
        owner = self.exclusive.get(item)

        if owner is not None and owner != tx:
            print(f"{tx}: Shared lock denied on {item}")
            return False

        self.shared.setdefault(item, set()).add(tx)
        print(f"{tx}: Shared lock acquired on {item}")
        return True

    def acquire_exclusive(self, tx, item):
        holders = self.shared.get(item, set()) - {tx}
        owner = self.exclusive.get(item)

        if holders or (owner is not None and owner != tx):
            print(f"{tx}: Exclusive lock denied on {item}")
            return False

        self.shared.get(item, set()).discard(tx)
        self.exclusive[item] = tx

        print(f"{tx}: Exclusive lock acquired on {item}")
        return True

    def release_all(self, tx):
        for item in list(self.shared):
            self.shared[item].discard(tx)

            if not self.shared[item]:
                del self.shared[item]

        for item in list(self.exclusive):
            if self.exclusive[item] == tx:
                del self.exclusive[item]

        print(f"{tx}: All locks released")


lm = LockManager()

lm.acquire_shared("T1", "A")
lm.acquire_shared("T2", "A")
lm.acquire_exclusive("T3", "A")

lm.release_all("T1")
lm.release_all("T2")

lm.acquire_exclusive("T3", "A")
lm.release_all("T3")
