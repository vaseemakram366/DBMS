# Multiple Granularity Locking
class LockManager:

    compatibility = {
        "IS": {"IS", "IX", "S", "SIX"},
        "IX": {"IS", "IX"},
        "S": {"IS", "S"},
        "SIX": {"IS"},
        "X": set()
    }

    def __init__(self):
        self.locks = {}

    def acquire(self, transaction, resource, mode):
        if resource not in self.locks:
            self.locks[resource] = []

        for tid, existing_mode in self.locks[resource]:

            if tid == transaction:
                continue

            if mode not in self.compatibility[existing_mode]:
                print(
                    transaction,
                    mode,
                    "on",
                    resource,
                    "-> BLOCKED"
                )
                return False

        self.locks[resource].append(
            (transaction, mode)
        )

        print(
            transaction,
            mode,
            "on",
            resource,
            "-> GRANTED"
        )

        return True

    def release(self, transaction, resource):

        if resource not in self.locks:
            return

        self.locks[resource] = [
            (tid, mode)
            for tid, mode in self.locks[resource]
            if tid != transaction
        ]

        print(
            transaction,
            "released",
            resource
        )

    def show_locks(self):

        print("\nCurrent Locks:")

        for resource, locks in self.locks.items():
            if locks:
                print(
                    resource,
                    "->",
                    locks
                )


lm = LockManager()

lm.acquire("T1", "Database", "IX")
lm.acquire("T1", "Students", "IX")
lm.acquire("T1", "Row1", "X")

lm.acquire("T2", "Database", "IS")
lm.acquire("T2", "Students", "IS")
lm.acquire("T2", "Row1", "S")

lm.show_locks()

lm.release("T1", "Row1")

lm.acquire("T2", "Row1", "S")

lm.show_locks()