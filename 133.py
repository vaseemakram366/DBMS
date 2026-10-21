# Lock Hierarchy Validator


class LockHierarchyValidator:

    REQUIRED_PARENT_LOCK = {
        "IS": {"IS", "IX", "S", "SIX", "X"},
        "IX": {"IX", "SIX", "X"},
        "S": {"S", "SIX", "X"},
        "SIX": {"SIX", "X"},
        "X": {"X"}
    }

    def __init__(self):
        self.locks = {}
        self.parents = {}

    def add_resource(self, resource, parent=None):
        self.parents[resource] = parent

    def acquire(self, tx, resource, mode):
        if mode not in self.REQUIRED_PARENT_LOCK:
            raise ValueError("Invalid lock mode")

        parent = self.parents.get(resource)

        if parent is not None:
            parent_mode = self.locks.get(parent, {}).get(tx)

            if parent_mode is None:
                print(
                    f"REJECTED: {tx} needs a parent lock "
                    f"on {parent} before locking {resource}"
                )
                return False

            allowed = self.REQUIRED_PARENT_LOCK[mode]

            if parent_mode not in allowed:
                print(
                    f"REJECTED: parent lock {parent_mode} "
                    f"is insufficient for child lock {mode}"
                )
                return False

        holders = self.locks.setdefault(resource, {})

        for owner, existing_mode in holders.items():
            if owner == tx:
                continue

            compatible = {
                "IS": {"IS", "IX", "S", "SIX"},
                "IX": {"IS", "IX"},
                "S": {"IS", "S"},
                "SIX": {"IS"},
                "X": set()
            }

            if mode not in compatible[existing_mode]:
                print(f"REJECTED: conflicting lock on {resource}")
                return False

        if tx in holders:
            print(f"REJECTED: {tx} already holds a lock on {resource}")
            return False

        holders[tx] = mode
        print(f"GRANTED: {tx} acquired {mode} on {resource}")
        return True

    def show_locks(self):
        print("\nLOCK TABLE")
        for resource, holders in self.locks.items():
            print(f"{resource}: {holders}")


validator = LockHierarchyValidator()

validator.add_resource("Database")
validator.add_resource("Employees", "Database")
validator.add_resource("Employee-101", "Employees")

# Missing parent intention locks
validator.acquire("T1", "Employee-101", "X")

# Acquire required locks from parent to child
validator.acquire("T1", "Database", "IX")
validator.acquire("T1", "Employees", "IX")
validator.acquire("T1", "Employee-101", "X")

validator.show_locks()
