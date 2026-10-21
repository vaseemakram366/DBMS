# Multi-Granularity Lock Manager


class MultiGranularityLockManager:

    COMPATIBILITY = {
        "IS": {"IS", "IX", "S", "SIX"},
        "IX": {"IS", "IX"},
        "S":  {"IS", "S"},
        "SIX": {"IS"},
        "X":  set()
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

            if mode not in self.COMPATIBILITY[existing_mode]:
                print(
                    f"DENIED: {tx} cannot acquire {mode} "
                    f"on {resource}; held by {owner} "
                    f"with {existing_mode}"
                )
                return False

        if tx in holders:
            print(f"{tx} already holds a lock on {resource}")
            return holders[tx] == mode

        holders[tx] = mode
        print(f"GRANTED: {tx} acquired {mode} on {resource}")
        return True

    def release(self, tx, resource):
        holders = self.locks.get(resource, {})

        if tx not in holders:
            print(f"{tx} holds no lock on {resource}")
            return

        del holders[tx]

        if not holders:
            del self.locks[resource]

        print(f"RELEASED: {tx} released lock on {resource}")

    def show_locks(self):
        print("\nCURRENT LOCK TABLE")

        if not self.locks:
            print("No active locks")
            return

        for resource, holders in self.locks.items():
            print(f"{resource}: {holders}")


manager = MultiGranularityLockManager()

manager.acquire("T1", "Employees", "IX")
manager.acquire("T1", "Employees.Row101", "X")

manager.acquire("T2", "Employees", "IS")
manager.acquire("T2", "Employees.Row102", "S")

manager.acquire("T2", "Employees.Row101", "S")

manager.show_locks()
