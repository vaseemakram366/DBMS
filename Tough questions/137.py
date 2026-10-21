# Multi-Granularity Lock Manager


class MultiGranularityLockManager:

    COMPATIBILITY = {
        "IS":  {"IS": True,  "IX": True,  "S": True,  "SIX": True,  "X": False},
        "IX":  {"IS": True,  "IX": True,  "S": False, "SIX": False, "X": False},
        "S":   {"IS": True,  "IX": False, "S": True,  "SIX": False, "X": False},
        "SIX": {"IS": True,  "IX": False, "S": False, "SIX": False, "X": False},
        "X":   {"IS": False, "IX": False, "S": False, "SIX": False, "X": False}
    }

    def __init__(self):
        self.locks = {}

    def acquire(self, tx, resource, mode):
        if mode not in self.COMPATIBILITY:
            raise ValueError("Invalid lock mode")

        holders = self.locks.setdefault(resource, {})

        for owner, existing_mode in holders.items():
            if owner == tx:
                continue

            if not self.COMPATIBILITY[existing_mode][mode]:
                print(
                    f"DENIED: {tx} requests {mode} on {resource}; "
                    f"conflicts with {owner}'s {existing_mode}"
                )
                return False

        holders[tx] = mode
        print(f"GRANTED: {tx} acquired {mode} on {resource}")
        return True

    def release_all(self, tx):
        for resource in list(self.locks):
            self.locks[resource].pop(tx, None)

            if not self.locks[resource]:
                del self.locks[resource]

        print(f"Released all locks for {tx}")

    def show_locks(self):
        print("\nACTIVE LOCKS")

        for resource, holders in self.locks.items():
            print(f"{resource}: {holders}")


manager = MultiGranularityLockManager()

manager.acquire("T1", "Database", "IX")
manager.acquire("T1", "Employees", "IX")
manager.acquire("T1", "Employees.Row101", "X")

manager.acquire("T2", "Database", "IS")
manager.acquire("T2", "Employees", "S")

manager.show_locks()

manager.release_all("T1")
manager.release_all("T2")
