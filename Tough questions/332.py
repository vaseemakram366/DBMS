# Timestamp-Based Concurrency Control


class TimestampProtocol:
    def __init__(self):
        self.read_ts = {"A": 0}
        self.write_ts = {"A": 0}

    def read(self, transaction, ts, item):
        if ts < self.write_ts[item]:
            print(f"{transaction}: READ rejected")
            return

        self.read_ts[item] = max(self.read_ts[item], ts)
        print(f"{transaction}: READ allowed on {item}")

    def write(self, transaction, ts, item):
        if ts < self.read_ts[item] or ts < self.write_ts[item]:
            print(f"{transaction}: WRITE rejected")
            return

        self.write_ts[item] = ts
        print(f"{transaction}: WRITE allowed on {item}")


db = TimestampProtocol()

db.read("T1", 5, "A")
db.write("T2", 10, "A")
db.read("T3", 7, "A")
db.write("T4", 15, "A")
