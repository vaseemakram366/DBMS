# Distributed Lock Manager

from collections import defaultdict


class LockManager:
    def __init__(self):
        self.locks = defaultdict(list)
        self.waiting = defaultdict(list)

    def compatible(self, transaction, item, lock_type):
        for holder, existing_type in self.locks[item]:
            if holder == transaction:
                continue

            if existing_type == "X" or lock_type == "X":
                return False

        return True

    def acquire(self, transaction, item, lock_type):
        if self.compatible(transaction, item, lock_type):
            self.locks[item].append(
                (transaction, lock_type)
            )

            print(
                f"{transaction} acquired "
                f"{lock_type} lock on {item}"
            )

            return True

        self.waiting[transaction].append(
            (item, lock_type)
        )

        print(
            f"{transaction} waiting for "
            f"{lock_type} lock on {item}"
        )

        return False

    def release(self, transaction, item):
        if item not in self.locks:
            return

        self.locks[item] = [
            (holder, lock_type)
            for holder, lock_type in self.locks[item]
            if holder != transaction
        ]

        if not self.locks[item]:
            del self.locks[item]

        print(
            f"{transaction} released lock on {item}"
        )

        self.process_waiting()

    def release_all(self, transaction):
        items = list(self.locks.keys())

        for item in items:
            self.release(transaction, item)

        if transaction in self.waiting:
            del self.waiting[transaction]

    def process_waiting(self):
        for transaction in list(self.waiting.keys()):
            requests = self.waiting[transaction]

            remaining = []

            for item, lock_type in requests:
                if self.compatible(
                    transaction,
                    item,
                    lock_type
                ):
                    self.locks[item].append(
                        (transaction, lock_type)
                    )

                    print(
                        f"{transaction} acquired "
                        f"waiting {lock_type} lock "
                        f"on {item}"
                    )
                else:
                    remaining.append(
                        (item, lock_type)
                    )

            if remaining:
                self.waiting[transaction] = remaining
            else:
                del self.waiting[transaction]

    def show_locks(self):
        print("\nCurrent Locks:")

        for item, holders in self.locks.items():
            print(item, "->", holders)

    def show_waiting(self):
        print("\nWaiting Transactions:")

        for transaction, requests in self.waiting.items():
            print(transaction, "->", requests)


lm = LockManager()

lm.acquire("T1", "A", "S")
lm.acquire("T2", "A", "S")

lm.acquire("T3", "A", "X")

lm.show_locks()
lm.show_waiting()

print("\nT1 commits")

lm.release_all("T1")

print("\nT2 commits")

lm.release_all("T2")

lm.show_locks()
lm.show_waiting()