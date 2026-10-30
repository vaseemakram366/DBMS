# Timestamp-Based Concurrency Control Simulator


class TimestampOrdering:
    def __init__(self, initial_data):
        self.data = initial_data.copy()
        self.read_ts = {item: 0 for item in initial_data}
        self.write_ts = {item: 0 for item in initial_data}
        self.transactions = {}

    def begin(self, tid, timestamp):
        self.transactions[tid] = {
            "timestamp": timestamp,
            "active": True
        }
        print(f"{tid} started with timestamp {timestamp}")

    def read(self, tid, item):
        if not self.transactions[tid]["active"]:
            print(f"{tid}: operation rejected; transaction inactive")
            return False

        ts = self.transactions[tid]["timestamp"]

        if ts < self.write_ts[item]:
            self.transactions[tid]["active"] = False
            print(f"{tid}: READ({item}) rejected; transaction aborted")
            return False

        self.read_ts[item] = max(self.read_ts[item], ts)
        print(f"{tid} read {item} = {self.data[item]}")
        return True

    def write(self, tid, item, value):
        if not self.transactions[tid]["active"]:
            print(f"{tid}: operation rejected; transaction inactive")
            return False

        ts = self.transactions[tid]["timestamp"]

        if ts < self.read_ts[item]:
            self.transactions[tid]["active"] = False
            print(f"{tid}: WRITE({item}) rejected; transaction aborted")
            return False

        if ts < self.write_ts[item]:
            self.transactions[tid]["active"] = False
            print(f"{tid}: WRITE({item}) rejected; transaction aborted")
            return False

        self.data[item] = value
        self.write_ts[item] = ts
        print(f"{tid} wrote {item} = {value}")
        return True

    def show_state(self):
        print("Database:", self.data)
        print("Read timestamps:", self.read_ts)
        print("Write timestamps:", self.write_ts)


db = TimestampOrdering({"A": 100})

db.begin("T1", 1)
db.begin("T2", 2)

db.read("T2", "A")
db.write("T2", "A", 200)

db.write("T1", "A", 150)

db.show_state()
