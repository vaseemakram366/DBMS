# Lock Compatibility Matrix Engine


class LockCompatibilityMatrix:

    def __init__(self):
        self.matrix = {
            "S": {"S": True, "X": False},
            "X": {"S": False, "X": False}
        }

        self.resource_locks = {}

    def is_compatible(self, existing_lock, requested_lock):
        return self.matrix[existing_lock][requested_lock]

    def request_lock(self, transaction_id, resource, lock_type):
        if lock_type not in ("S", "X"):
            raise ValueError("Lock type must be S or X")

        locks = self.resource_locks.setdefault(resource, [])

        for owner, existing_type in locks:
            if owner == transaction_id:
                continue

            if not self.is_compatible(existing_type, lock_type):
                print(
                    f"DENIED: {transaction_id} requests {lock_type} "
                    f"on {resource}; blocked by {owner}'s {existing_type} lock."
                )
                return False

        if (transaction_id, lock_type) not in locks:
            locks.append((transaction_id, lock_type))

        print(
            f"GRANTED: {transaction_id} receives {lock_type} lock "
            f"on {resource}."
        )
        return True

    def release_locks(self, transaction_id):
        for resource in list(self.resource_locks):
            self.resource_locks[resource] = [
                (owner, lock_type)
                for owner, lock_type in self.resource_locks[resource]
                if owner != transaction_id
            ]

            if not self.resource_locks[resource]:
                del self.resource_locks[resource]

        print(f"Released all locks held by {transaction_id}.")


engine = LockCompatibilityMatrix()

engine.request_lock("T1", "Account-A", "S")
engine.request_lock("T2", "Account-A", "S")
engine.request_lock("T3", "Account-A", "X")

engine.release_locks("T1")

engine.request_lock("T3", "Account-A", "X")
