# Wait-Die Deadlock Prevention


class WaitDie:
    def __init__(self):
        self.timestamp = {
            "T1": 1,
            "T2": 2,
            "T3": 3,
            "T4": 4
        }

    def request_lock(self, requester, holder):
        print(f"{requester} requests lock held by {holder}")

        if self.timestamp[requester] < self.timestamp[holder]:
            print(f"{requester}: WAIT")
        else:
            print(f"{requester}: DIE (ABORT)")

db = WaitDie()

db.request_lock("T1", "T2")
db.request_lock("T4", "T3")
