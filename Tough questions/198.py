# Optimistic Concurrency Control Simulator


class OptimisticConcurrencyControl:
    def __init__(self, initial_data):
        self.database = initial_data.copy()
        self.version = {item: 0 for item in initial_data}
        self.transactions = {}
        self.next_id = 1

    def begin(self):
        tid = f"T{self.next_id}"
        self.next_id += 1

        self.transactions[tid] = {
            "read_versions": {},
            "writes": {},
            "active": True
        }

        print(f"{tid} started")
        return tid

    def read(self, tid, item):
        tx = self.transactions[tid]

        if not tx["active"]:
            print(f"{tid}: transaction inactive")
            return None

        tx["read_versions"].setdefault(item, self.version[item])

        value = tx["writes"].get(item, self.database[item])
        print(f"{tid} read {item} = {value}")
        return value

    def write(self, tid, item, value):
        tx = self.transactions[tid]

        if not tx["active"]:
            print(f"{tid}: transaction inactive")
            return False

        if item not in tx["read_versions"]:
            self.read(tid, item)

        tx["writes"][item] = value
        print(f"{tid} prepared WRITE {item} = {value}")
        return True

    def commit(self, tid):
        tx = self.transactions[tid]

        if not tx["active"]:
            print(f"{tid}: commit rejected")
            return False

        for item, read_version in tx["read_versions"].items():
            if self.version[item] != read_version:
                tx["active"] = False
                print(f"{tid}: validation failed on {item}; aborted")
                return False

        for item, value in tx["writes"].items():
            self.database[item] = value
            self.version[item] += 1

        tx["active"] = False
        print(f"{tid} committed successfully")
        return True

    def show_database(self):
        print("Database:", self.database)
        print("Versions:", self.version)


db = OptimisticConcurrencyControl({"A": 100})

t1 = db.begin()
t2 = db.begin()

db.read(t1, "A")
db.read(t2, "A")

db.write(t1, "A", 150)
db.write(t2, "A", 200)

db.commit(t1)
db.commit(t2)

db.show_database()
