# Wait-Die Deadlock Prevention Algorithm


class WaitDie:
    def __init__(self):
        self.timestamp = {
            "T1": 1,
            "T2": 2
        }

    def request(self, requester, holder):
        if self.timestamp[requester] < self.timestamp[holder]:
            print(f"{requester} (older) waits for {holder} (younger)")
        else:
            print(f"{requester} (younger) aborts (dies)")


wd = WaitDie()

wd.request("T1", "T2")
wd.request("T2", "T1")
