# Wait-Die Deadlock Prevention

class WaitDie:

    def __init__(self):
        self.timestamp = {}

    def add_transaction(self, transaction, timestamp):
        self.timestamp[transaction] = timestamp

    def request(self, transaction, holder):
        t1 = self.timestamp[transaction]
        t2 = self.timestamp[holder]

        print(
            f"\n{transaction} requests resource "
            f"held by {holder}"
        )

        if t1 < t2:
            print(
                transaction,
                "is older -> WAIT"
            )
        else:
            print(
                transaction,
                "is younger -> DIE (ROLLBACK)"
            )


wd = WaitDie()

wd.add_transaction("T1", 1)
wd.add_transaction("T2", 2)
wd.add_transaction("T3", 3)

wd.request("T1", "T2")
wd.request("T3", "T1")