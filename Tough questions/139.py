# Strict Two-Phase Locking (Strict 2PL)


class Strict2PLManager:
    def __init__(self):
        self.transactions = {}
        self.lock_table = {}

    def begin(self, tx):
        if tx in self.transactions:
            print(f"{tx} already exists")
            return

        self.transactions[tx] = {
            "phase": "GROWING",
            "locks": {}
        }
        print(f"{tx} started")

    def acquire_lock(self, tx, resource, mode):
        if tx not in self.transactions:
            print(f"{tx} does not exist")
            return False

        if mode not in ("S", "X"):
            print("Invalid lock mode")
            return False

        transaction = self.transactions[tx]

        if transaction["phase"] != "GROWING":
            print(f"{tx}: cannot acquire new locks")
            return False

        holders = self.lock_table.get(resource, {})

        # Check compatibility with other transactions
        for other_tx, other_mode in holders.items():
            if other_tx == tx:
                continue

            if mode == "X" or other_mode == "X":
                print(f"{tx}: lock conflict on {resource}")
                return False

        current_mode = transaction["locks"].get(resource)

        # Upgrade shared lock to exclusive lock
        if current_mode == "S" and mode == "X":
            transaction["locks"][resource] = "X"
            self.lock_table[resource][tx] = "X"
            print(f"{tx}: upgraded to X lock on {resource}")
            return True

        if current_mode == "X" or current_mode == "S":
            print(f"{tx}: already holds {current_mode} lock on {resource}")
            return True

        transaction["locks"][resource] = mode
        self.lock_table.setdefault(resource, {})[tx] = mode

        print(f"{tx}: acquired {mode} lock on {resource}")
        return True

    def release_lock(self, tx, resource):
        if tx not in self.transactions:
            print(f"{tx} does not exist")
            return False

        transaction = self.transactions[tx]
        mode = transaction["locks"].get(resource)

        if mode is None:
            print(f"{tx}: no lock held on {resource}")
            return False

        # Strict 2PL: X locks stay until transaction ends
        if mode == "X":
            print(f"{tx}: cannot release X lock before COMMIT/ROLLBACK")
            return False

        del transaction["locks"][resource]
        del self.lock_table[resource][tx]

        if not self.lock_table[resource]:
            del self.lock_table[resource]

        transaction["phase"] = "SHRINKING"
        print(f"{tx}: released S lock on {resource}")
        return True

    def _end_transaction(self, tx, action):
        if tx not in self.transactions:
            print(f"{tx} does not exist")
            return

        transaction = self.transactions[tx]

        for resource in list(transaction["locks"]):
            del self.lock_table[resource][tx]

            if not self.lock_table[resource]:
                del self.lock_table[resource]

        del self.transactions[tx]
        print(f"{tx}: {action}; all locks released")

    def commit(self, tx):
        self._end_transaction(tx, "COMMIT")

    def rollback(self, tx):
        self._end_transaction(tx, "ROLLBACK")


# Demonstration
db = Strict2PLManager()

db.begin("T1")
db.acquire_lock("T1", "Account-A", "X")

db.release_lock("T1", "Account-A")

db.begin("T2")
db.acquire_lock("T2", "Account-A", "X")

db.commit("T1")

db.acquire_lock("T2", "Account-A", "X")
db.commit("T2")
