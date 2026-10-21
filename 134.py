# Lock Manager Consistency Checker


class LockManagerConsistencyChecker:

    VALID_MODES = {"IS", "IX", "S", "SIX", "X"}

    def __init__(self):
        self.transactions = {}
        self.locks = {}

    def add_transaction(self, tx_id, status="ACTIVE"):
        self.transactions[tx_id] = {
            "status": status,
            "held_locks": set()
        }

    def assign_lock(self, tx_id, resource, mode):
        self.locks.setdefault(resource, {})[tx_id] = mode

        if tx_id in self.transactions:
            self.transactions[tx_id]["held_locks"].add(
                (resource, mode)
            )

    def check_consistency(self):
        errors = []

        # Check lock records against transaction records.
        for resource, holders in self.locks.items():
            for tx_id, mode in holders.items():

                if tx_id not in self.transactions:
                    errors.append(
                        f"Unknown transaction {tx_id} holds "
                        f"a lock on {resource}"
                    )
                    continue

                if mode not in self.VALID_MODES:
                    errors.append(
                        f"Invalid lock mode {mode} on {resource}"
                    )

                tx = self.transactions[tx_id]

                if tx["status"] != "ACTIVE":
                    errors.append(
                        f"Inactive transaction {tx_id} still holds "
                        f"a lock on {resource}"
                    )

                if (resource, mode) not in tx["held_locks"]:
                    errors.append(
                        f"Lock record missing from transaction "
                        f"{tx_id}: {resource}/{mode}"
                    )

        # Check transaction records against lock records.
        for tx_id, tx in self.transactions.items():
            for resource, mode in tx["held_locks"]:
                actual_mode = (
                    self.locks.get(resource, {}).get(tx_id)
                )

                if actual_mode is None:
                    errors.append(
                        f"Transaction {tx_id} records a lock on "
                        f"{resource}, but lock manager does not"
                    )
                elif actual_mode != mode:
                    errors.append(
                        f"Lock mode mismatch for {tx_id} on "
                        f"{resource}: transaction={mode}, "
                        f"manager={actual_mode}"
                    )

        return errors

    def report(self):
        errors = self.check_consistency()

        print("LOCK MANAGER CONSISTENCY REPORT")
        print("-" * 40)

        if not errors:
            print("PASS: All lock records are consistent.")
            return

        print(f"FAIL: Found {len(errors)} inconsistency issue(s).")

        for number, error in enumerate(errors, start=1):
            print(f"{number}. {error}")


checker = LockManagerConsistencyChecker()

checker.add_transaction("T1")
checker.add_transaction("T2", status="COMMITTED")

checker.assign_lock("T1", "Employees", "X")
checker.assign_lock("T2", "Accounts", "S")

# Simulate an orphan lock record.
checker.locks.setdefault("Payroll", {})["T99"] = "X"

# Simulate a transaction record missing its lock entry.
checker.transactions["T1"]["held_locks"].add(
    ("Orders", "S")
)

checker.report()
