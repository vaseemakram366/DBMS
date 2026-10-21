# Database Two-Phase Locking (2PL) Manager


class TwoPhaseLockingManager:

    def __init__(self):
        self.transactions = {}
        self.lock_table = {}

    def begin(self, tx_id):
        if tx_id in self.transactions:
            print(f"{tx_id} already exists.")
            return

        self.transactions[tx_id] = {
            "phase": "GROWING",
            "locks": set()
        }

        print(f"{tx_id} started in GROWING phase.")

    def acquire_lock(self, tx_id, resource):
        tx = self.transactions.get(tx_id)

        if tx is None:
            print(f"DENIED: {tx_id} does not exist.")
            return False

        if tx["phase"] != "GROWING":
            print(f"DENIED: {tx_id} cannot acquire locks in SHRINKING phase.")
            return False

        owner = self.lock_table.get(resource)

        if owner is not None and owner != tx_id:
            print(f"BLOCKED: {resource} is held by {owner}.")
            return False

        self.lock_table[resource] = tx_id
        tx["locks"].add(resource)

        print(f"{tx_id} acquired lock on {resource}.")
        return True

    def release_lock(self, tx_id, resource):
        tx = self.transactions.get(tx_id)

        if tx is None or resource not in tx["locks"]:
            print(f"DENIED: {tx_id} does not hold {resource}.")
            return False

        del self.lock_table[resource]
        tx["locks"].remove(resource)
        tx["phase"] = "SHRINKING"

        print(f"{tx_id} released {resource}.")
        print(f"{tx_id} entered SHRINKING phase.")

        return True

    def commit(self, tx_id):
        tx = self.transactions.get(tx_id)

        if tx is None:
            print(f"DENIED: {tx_id} does not exist.")
            return

        for resource in list(tx["locks"]):
            del self.lock_table[resource]

        del self.transactions[tx_id]
        print(f"{tx_id} committed; all locks released.")


manager = TwoPhaseLockingManager()

manager.begin("T1")
manager.acquire_lock("T1", "Account-A")
manager.acquire_lock("T1", "Account-B")

manager.release_lock("T1", "Account-A")

# This request violates 2PL.
manager.acquire_lock("T1", "Account-C")

manager.commit("T1")
