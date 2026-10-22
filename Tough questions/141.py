# Deadlock Prevention — Wait-Die & Wound-Wait


class DeadlockPrevention:
    def __init__(self, policy):
        self.policy = policy
        self.timestamp = {}
        self.active = set()
        self.locks = {}
        self.waiting = {}
        self.next_timestamp = 0

    def begin(self, tx):
        self.timestamp[tx] = self.next_timestamp
        self.next_timestamp += 1
        self.active.add(tx)
        print(f"{tx} started, timestamp={self.timestamp[tx]}")

    def request_lock(self, tx, resource):
        if tx not in self.active:
            print(f"{tx} is not active")
            return

        owner = self.locks.get(resource)

        if owner is None:
            self.locks[resource] = tx
            self.waiting.pop(tx, None)
            print(f"{tx} acquired X lock on {resource}")
            return

        if owner == tx:
            print(f"{tx} already holds {resource}")
            return

        older = self.timestamp[tx] < self.timestamp[owner]

        if self.policy == "wait-die":
            if older:
                self.waiting[tx] = owner
                print(f"{tx} waits for {owner} (older transaction)")
            else:
                print(f"{tx} dies: younger than {owner}")
                self.abort(tx)

        elif self.policy == "wound-wait":
            if older:
                print(f"{tx} wounds {owner} (older transaction)")
                self.abort(owner)
                self.locks[resource] = tx
                self.waiting.pop(tx, None)
                print(f"{tx} acquired X lock on {resource}")
            else:
                self.waiting[tx] = owner
                print(f"{tx} waits for {owner} (younger transaction)")

    def abort(self, tx):
        if tx not in self.active:
            return

        # Release all locks owned by the aborted transaction
        for resource, owner in list(self.locks.items()):
            if owner == tx:
                del self.locks[resource]

        self.active.remove(tx)
        self.waiting.pop(tx, None)

        # Remove waiting entries that point to the aborted transaction
        for waiter, owner in list(self.waiting.items()):
            if owner == tx:
                del self.waiting[waiter]

        print(f"{tx} aborted; its locks released")

    def commit(self, tx):
        if tx not in self.active:
            print(f"{tx} is not active")
            return

        for resource, owner in list(self.locks.items()):
            if owner == tx:
                del self.locks[resource]

        self.active.remove(tx)
        self.waiting.pop(tx, None)
        print(f"{tx} committed; its locks released")


# Demonstrate WAIT-DIE
print("=== WAIT-DIE ===")
db1 = DeadlockPrevention("wait-die")
db1.begin("T1")
db1.begin("T2")
db1.request_lock("T2", "Account-A")
db1.request_lock("T1", "Account-A")

# Demonstrate WOUND-WAIT
print("\n=== WOUND-WAIT ===")
db2 = DeadlockPrevention("wound-wait")
db2.begin("T1")
db2.begin("T2")
db2.request_lock("T2", "Account-A")
db2.request_lock("T1", "Account-A")
