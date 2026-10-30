# MVCC Snapshot Isolation Simulator in Python


class SnapshotIsolationSimulator:
    def __init__(self, initial_data):
        self.database = {
            key: [(0, value)]
            for key, value in initial_data.items()
        }
        self.clock = 0
        self.next_id = 1
        self.transactions = {}

    def begin(self):
        tid = f"T{self.next_id}"
        self.next_id += 1

        self.transactions[tid] = {
            "start_ts": self.clock,
            "writes": {},
            "active": True
        }

        print(f"{tid} started with snapshot ts={self.clock}")
        return tid

    def read(self, tid, item):
        tx = self.transactions[tid]

        if not tx["active"]:
            print(f"{tid} cannot read: transaction inactive")
            return None

        if item in tx["writes"]:
            value = tx["writes"][item]
        else:
            visible = [
                (ts, value)
                for ts, value in self.database[item]
                if ts <= tx["start_ts"]
            ]

            if not visible:
                print(f"{tid}: no visible version of {item}")
                return None

            value = visible[-1][1]

        print(
            f"{tid} reads {item} = {value} "
            f"(snapshot ts={tx['start_ts']})"
        )
        return value

    def write(self, tid, item, value):
        tx = self.transactions[tid]

        if not tx["active"]:
            print(f"{tid} cannot write: transaction inactive")
            return

        if item not in self.database:
            print(f"{tid}: unknown item {item}")
            return

        tx["writes"][item] = value
        print(f"{tid} stages {item} = {value}")

    def commit(self, tid):
        tx = self.transactions[tid]

        if not tx["active"]:
            print(f"{tid} cannot commit: transaction inactive")
            return False

        for item in tx["writes"]:
            latest_ts = self.database[item][-1][0]

            if latest_ts > tx["start_ts"]:
                tx["active"] = False
                print(f"{tid} aborted: write conflict on {item}")
                return False

        self.clock += 1

        for item, value in tx["writes"].items():
            self.database[item].append((self.clock, value))

        tx["active"] = False
        print(f"{tid} committed at ts={self.clock}")
        return True

    def show_database(self):
        current = {
            item: versions[-1][1]
            for item, versions in self.database.items()
        }

        print("Current database:", current)
        print("All versions:", self.database)


db = SnapshotIsolationSimulator({"A": 100})

t1 = db.begin()
t2 = db.begin()

db.read(t1, "A")
db.read(t2, "A")

db.write(t1, "A", 150)
db.commit(t1)

db.read(t2, "A")
db.write(t2, "A", 200)
db.commit(t2)

db.show_database()
