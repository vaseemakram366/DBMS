# Deadlock Prevention Using Wound-Wait Scheme


class WoundWaitScheme:
    def __init__(self):
        self.timestamps = {
            "T1": 1,
            "T2": 2,
            "T3": 3,
            "T4": 4
        }

    def request_lock(self, requester, holder):
        print(f"{requester} requests lock held by {holder}")

        if self.timestamps[requester] < self.timestamps[holder]:
            print(f"{requester} is older: WOUND {holder} (ABORT)")
        else:
            print(f"{requester} is younger: WAIT")


db = WoundWaitScheme()

db.request_lock("T1", "T2")
db.request_lock("T4", "T3")
