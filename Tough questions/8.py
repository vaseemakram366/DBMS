# 3. Wound-Wait Deadlock Prevention

class WoundWait:

    def __init__(self):
        self.timestamp = {}

    def add_transaction(self, transaction, timestamp):
        self.timestamp[transaction] = timestamp

    def request(self, transaction, holder):

        requester_time = self.timestamp[transaction]
        holder_time = self.timestamp[holder]

        print(
            f"\n{transaction} requests resource "
            f"held by {holder}"
        )

        if requester_time < holder_time:
            print(
                transaction,
                "is older -> WOUND",
                holder
            )
            print(holder, "must rollback")

        else:
            print(
                transaction,
                "is younger -> WAIT"
            )


ww = WoundWait()

ww.add_transaction("T1", 1)
ww.add_transaction("T2", 2)
ww.add_transaction("T3", 3)

ww.request("T1", "T2")
ww.request("T3", "T1")