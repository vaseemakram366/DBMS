# Strict Two-Phase Locking Simulator


class Strict2PL:
    def __init__(self):
        self.locks = {}
        self.transactions = {}

    def begin(self, transaction):
        self.transactions[transaction] = []
        print(f"{transaction} started")

    def acquire_lock(self, transaction, item):
        if item in self.locks:
            print(f"{transaction}: Lock DENIED on {item}")
            return

        self.locks[item] = transaction
        self.transactions[transaction].append(item)

        print(f"{transaction}: X Lock acquired on {item}")

    def commit(self, transaction):
        print(f"{transaction} committed")

        for item in self.transactions[transaction]:
            if self.locks.get(item) == transaction:
                del self.locks[item]

        self.transactions[transaction] = []
        print(f"Locks released for {transaction}")


db = Strict2PL()

db.begin("T1")
db.acquire_lock("T1", "A")

db.begin("T2")
db.acquire_lock("T2", "A")

db.commit("T1")

db.acquire_lock("T2", "A")
db.commit("T2")
