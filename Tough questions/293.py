# Deadlock Prevention Using Wait-Die Scheme


class WaitDieScheme:
    def __init__(self):
        self.timestamps = {
            "T1": 1,
            "T2": 2
        }

    def request_lock(self, requester, holder):
        requester_time = self.timestamps[requester]
        holder_time = self.timestamps[holder]

        print(requester, "requests lock held by", holder)

        if requester_time < holder_time:
            print(requester, "is older: WAIT")
        else:
            print(requester, "is younger: DIE (ABORT)")


db = WaitDieScheme()

db.request_lock("T1", "T2")
db.request_lock("T2", "T1")
