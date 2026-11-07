# Thomas Write Rule


class ThomasWriteRule:
    def __init__(self):
        self.timestamp = {
            "T1": 1,
            "T2": 2
        }

        self.read_ts = {"A": 0}
        self.write_ts = {"A": 0}
        self.data = {"A": 0}

    def write(self, transaction, item, value):
        ts = self.timestamp[transaction]

        if ts < self.read_ts[item]:
            print(f"{transaction}: ABORT")
            return

        if ts < self.write_ts[item]:
            print(
                f"{transaction}: WRITE ignored "
                "(obsolete operation)"
            )
            return

        self.data[item] = value
        self.write_ts[item] = ts

        print(
            f"{transaction}: WRITE {item} = {value}: SUCCESS"
        )


db = ThomasWriteRule()

db.write("T1", "A", 100)
db.write("T2", "A", 200)
db.write("T1", "A", 150)

print("Final Database:", db.data)
