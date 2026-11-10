# Wound-Wait Deadlock Prevention Algorithm


class WoundWait:
    def __init__(self):
        self.timestamp = {
            "T1": 1,
            "T2": 2
        }

    def request(self, requester, holder):
        if self.timestamp[requester] < self.timestamp[holder]:
            print(f"{requester} (older) wounds {holder} (younger)")
        else:
            print(f"{requester} (younger) waits for {holder} (older)")


ww = WoundWait()

ww.request("T1", "T2")
ww.request("T2", "T1")
