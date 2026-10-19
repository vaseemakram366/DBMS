# Lock Upgrade and Downgrade Manager


class LockUpgradeDowngradeManager:

    def __init__(self):
        self.locks = {}

    def acquire_shared(self, tx, resource):
        holders = self.locks.setdefault(resource, {})

        if any(
            owner != tx and lock_type == "X"
            for owner, lock_type in holders.items()
        ):
            print(f"DENIED: {tx} cannot acquire S on {resource}")
            return False

        if holders.get(tx) == "X":
            print(f"{tx} already holds X on {resource}")
            return True

        holders[tx] = "S"
        print(f"GRANTED: {tx} acquired S on {resource}")
        return True

    def acquire_exclusive(self, tx, resource):
        holders = self.locks.setdefault(resource, {})

        if any(owner != tx for owner in holders):
            print(f"DENIED: {tx} cannot acquire X on {resource}")
            return False

        holders[tx] = "X"
        print(f"GRANTED: {tx} acquired X on {resource}")
        return True

    def upgrade(self, tx, resource):
        holders = self.locks.get(resource, {})

        if holders.get(tx) != "S":
            print(f"DENIED: {tx} must hold S before upgrading")
            return False

        if any(owner != tx for owner in holders):
            print(f"UPGRADE BLOCKED: other transactions hold locks")
            return False

        holders[tx] = "X"
        print(f"UPGRADED: {tx} changed S to X on {resource}")
        return True

    def downgrade(self, tx, resource):
        holders = self.locks.get(resource, {})

        if holders.get(tx) != "X":
            print(f"DENIED: {tx} does not hold X on {resource}")
            return False

        holders[tx] = "S"
        print(f"DOWNGRADED: {tx} changed X to S on {resource}")
        return True

    def release(self, tx, resource):
        holders = self.locks.get(resource, {})

        if tx in holders:
            del holders[tx]
            print(f"RELEASED: {tx} released lock on {resource}")

        if not holders and resource in self.locks:
            del self.locks[resource]


manager = LockUpgradeDowngradeManager()

manager.acquire_shared("T1", "Account-A")
manager.acquire_shared("T2", "Account-A")

manager.upgrade("T1", "Account-A")

manager.release("T2", "Account-A")
manager.upgrade("T1", "Account-A")

manager.downgrade("T1", "Account-A")
