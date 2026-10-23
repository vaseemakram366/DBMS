# Transaction Rollback & Lock Recovery Manager


from collections import deque


class TransactionRecoveryManager:
    def __init__(self):
        self.data = {"Account-A": 1000}
        self.transactions = {}
        self.lock_table = {}
        self.wait_queues = {}

    def begin(self, tx):
        self.transactions[tx] = {
            "status": "ACTIVE",
            "undo_log": [],
            "locks": set()
        }
        print(f"{tx} started")

    def write(self, tx, resource, new_value):
        if tx not in self.transactions:
            print(f"{tx} does not exist")
            return

        if self.transactions[tx]["status"] != "ACTIVE":
            print(f"{tx} is not active")
            return

        owner = self.lock_table.get(resource)

        if owner is not None and owner != tx:
            self.wait_queues.setdefault(resource, deque()).append(tx)
            print(f"{tx} waiting for {resource}, held by {owner}")
            return

        self.lock_table[resource] = tx
        self.transactions[tx]["locks"].add(resource)

        old_value = self.data[resource]
        self.transactions[tx]["undo_log"].append(
            (resource, old_value)
        )

        self.data[resource] = new_value
        print(f"{tx}: {resource} changed from {old_value} to {new_value}")

    def rollback(self, tx):
        if tx not in self.transactions:
            print(f"{tx} does not exist")
            return

        transaction = self.transactions[tx]

        if transaction["status"] != "ACTIVE":
            print(f"{tx} is not active")
            return

        # Undo changes in reverse order
        for resource, old_value in reversed(transaction["undo_log"]):
            self.data[resource] = old_value
            print(f"UNDO {tx}: {resource} restored to {old_value}")

        transaction["undo_log"].clear()
        transaction["status"] = "ABORTED"

        # Release locks and grant them to eligible waiters
        for resource in list(transaction["locks"]):
            if self.lock_table.get(resource) == tx:
                del self.lock_table[resource]

            transaction["locks"].remove(resource)
            self._grant_waiter(resource)

        print(f"{tx} aborted")
        print("Current data:", self.data)

    def _grant_waiter(self, resource):
        queue = self.wait_queues.get(resource)

        while queue:
            next_tx = queue.popleft()

            if (
                next_tx in self.transactions
                and self.transactions[next_tx]["status"] == "ACTIVE"
            ):
                self.lock_table[resource] = next_tx
                self.transactions[next_tx]["locks"].add(resource)
                print(f"{next_tx} granted lock on {resource}")
                break

        if queue is not None and not queue:
            self.wait_queues.pop(resource, None)

    def commit(self, tx):
        if tx not in self.transactions:
            print(f"{tx} does not exist")
            return

        transaction = self.transactions[tx]

        if transaction["status"] != "ACTIVE":
            print(f"{tx} is not active")
            return

        transaction["status"] = "COMMITTED"
        transaction["undo_log"].clear()

        for resource in list(transaction["locks"]):
            if self.lock_table.get(resource) == tx:
                del self.lock_table[resource]

            transaction["locks"].remove(resource)
            self._grant_waiter(resource)

        print(f"{tx} committed")


# Demonstration
db = TransactionRecoveryManager()

db.begin("T1")
db.write("T1", "Account-A", 800)

db.begin("T2")
db.write("T2", "Account-A", 500)

print("\nDeadlock victim selected: T1")
db.rollback("T1")

db.write("T2", "Account-A", 500)
db.commit("T2")
