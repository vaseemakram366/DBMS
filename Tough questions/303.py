# Timestamp Ordering Protocol


class TimestampOrdering:
    def __init__(self):
        self.timestamp = {
            "T1": 1,
            "T2": 2
        }

        self.read_ts = {"A": 0}
        self.write_ts = {"A": 0}
        self.data = {"A": 0}

    def read(self, transaction, item):
        ts = self.timestamp[transaction]

        if ts < self.write_ts[item]:
            print(f"{transaction} READ {item}: ABORT")
            return

        self.read_ts[item] = max(
            self.read_ts[item], ts
        )

        print(
            f"{transaction} READ {item} = "
            f"{self.data[item]}: SUCCESS"
        )

    def write(self, transaction, item, value):
        ts = self.timestamp[transaction]

        if ts < self.read_ts[item]:
            print(f"{transaction} WRITE {item}: ABORT")
            return

        if ts < self.write_ts[item]:
            print(f"{transaction} WRITE {item}: ABORT")
            return

        self.data[item] = value
        self.write_ts[item] = ts

        print(
            f"{transaction} WRITE {item} = {value}: SUCCESS"
        )


db = TimestampOrdering()

db.write("T1", "A", 100)
db.read("T2", "A")
db.write("T2", "A", 200)
db.read("T1", "A")
