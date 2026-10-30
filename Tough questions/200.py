# MVCC Version Cleanup Simulator in Python


class MVCCVersionCleanup:
    def __init__(self, initial_data):
        self.database = {
            item: [(0, value)]
            for item, value in initial_data.items()
        }
        self.clock = 0
        self.next_id = 1
        self.transactions = {}

    def update(self, item, value):
        self.clock += 1
        self.database[item].append((self.clock, value))
        print(f"Updated {item} = {value} at ts={self.clock}")

    def begin(self):
        tid = f"T{self.next_id}"
        self.next_id += 1

        self.transactions[tid] = {
            "snapshot": self.clock,
            "active": True
        }

        print(
            f"{tid} started with snapshot ts={self.clock}"
        )
        return tid

    def finish(self, tid):
        if tid in self.transactions:
            self.transactions[tid]["active"] = False
            print(f"{tid} finished")

    def cleanup(self):
        active_snapshots = [
            tx["snapshot"]
            for tx in self.transactions.values()
            if tx["active"]
        ]

        print("Active snapshots:", active_snapshots)

        for item, versions in self.database.items():
            if not active_snapshots:
                self.database[item] = versions[-1:]
                continue

            oldest_snapshot = min(active_snapshots)

            # Keep the newest version visible to the oldest
            # active snapshot, plus every newer version.
            keep_index = 0

            for i, (ts, value) in enumerate(versions):
                if ts <= oldest_snapshot:
                    keep_index = i
                else:
                    break

            self.database[item] = versions[keep_index:]

        print("Cleanup completed")

    def show_versions(self):
        print("Stored versions:", self.database)


db = MVCCVersionCleanup({"A": 100})

db.update("A", 150)
t1 = db.begin()

db.update("A", 200)
db.update("A", 300)

db.show_versions()

db.cleanup()
db.show_versions()

db.finish(t1)

db.cleanup()
db.show_versions()
