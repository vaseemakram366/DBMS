# Lock Conversion (Upgrade and Downgrade)


class LockConversion:
    def __init__(self):
        self.locks = {}

    def acquire(self, transaction, item, mode):
        self.locks.setdefault(item, {})
        self.locks[item][transaction] = mode
        print(f"{transaction} acquired {mode} lock on {item}")

    def upgrade(self, transaction, item):
        current = self.locks[item]

        if current.get(transaction) != "S":
            print("Upgrade denied: Shared lock not found")
            return

        if len(current) > 1:
            print("Upgrade denied: Other locks exist")
            return

        current[transaction] = "X"
        print(f"{transaction}: S -> X upgrade successful")

    def downgrade(self, transaction, item):
        current = self.locks[item]

        if current.get(transaction) != "X":
            print("Downgrade denied: Exclusive lock not found")
            return

        current[transaction] = "S"
        print(f"{transaction}: X -> S downgrade successful")


db = LockConversion()

db.acquire("T1", "A", "S")
db.upgrade("T1", "A")
db.downgrade("T1", "A")
