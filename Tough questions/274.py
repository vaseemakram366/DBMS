# Distributed Lock Management


class DistributedLockManager:
    def __init__(self):
        self.locks = {}

    def acquire_lock(self, resource, transaction):
        if resource not in self.locks:
            self.locks[resource] = transaction
            print(transaction, "acquired lock on", resource)
        else:
            print(
                transaction,
                "cannot acquire lock on",
                resource
            )

    def release_lock(self, resource, transaction):
        if self.locks.get(resource) == transaction:
            del self.locks[resource]
            print(transaction, "released lock on", resource)
        else:
            print("Lock release failed")


manager = DistributedLockManager()

manager.acquire_lock("Database", "T1")
manager.acquire_lock("Database", "T2")
manager.release_lock("Database", "T1")
manager.acquire_lock("Database", "T2")
