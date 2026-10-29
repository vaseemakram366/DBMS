# Database Checkpoint Simulator


class DatabaseCheckpointSimulator:
    def __init__(self):
        self.disk = {"A": 100, "B": 200}
        self.buffer = self.disk.copy()
        self.log = []
        self.next_lsn = 1
        self.checkpoint_lsn = 0
        self.active = set()
        self.locks = {}

    def add_log(self, op, tid=None, item=None, old=None, new=None):
        record = {
            "lsn": self.next_lsn,
            "op": op,
            "tid": tid,
            "item": item,
            "old": old,
            "new": new
        }
        self.log.append(record)
        self.next_lsn += 1
        return record["lsn"]

    def begin(self, tid):
        self.add_log("BEGIN", tid)
        self.active.add(tid)
        print(f"{tid} BEGIN (LSN {self.next_lsn - 1})")

    def write(self, tid, item, value):
        if tid not in self.active:
            raise ValueError("Transaction is not active")

        if item in self.locks and self.locks[item] != tid:
            raise ValueError("Item is locked by another transaction")

        self.locks[item] = tid
        old = self.buffer[item]
        self.buffer[item] = value

        lsn = self.add_log("WRITE", tid, item, old, value)
        print(f"{tid} WRITE {item}: {old} -> {value} (LSN {lsn})")

    def flush_page(self, item):
        self.disk[item] = self.buffer[item]
        print(f"FLUSH {item} = {self.disk[item]}")

    def commit(self, tid):
        self.add_log("COMMIT", tid)
        self.active.remove(tid)

        for item in list(self.locks):
            if self.locks[item] == tid:
                del self.locks[item]

        print(f"{tid} COMMIT (LSN {self.next_lsn - 1})")

    def checkpoint(self):
        if self.active:
            raise ValueError(
                "Quiescent checkpoint requires no active transactions"
            )

        self.disk = self.buffer.copy()
        lsn = self.add_log("CHECKPOINT")
        self.checkpoint_lsn = lsn

        print(
            "CHECKPOINT: all pages flushed; "
            f"checkpoint LSN = {lsn}"
        )

    def crash(self):
        print("\n*** CRASH ***")
        self.buffer = self.disk.copy()
        self.active.clear()
        self.locks.clear()
        print(f"Disk before recovery: {self.disk}")

    def recover(self):
        print(
            f"\nRecovery starts after checkpoint LSN "
            f"{self.checkpoint_lsn}"
        )

        records = [
            r for r in self.log
            if r["lsn"] > self.checkpoint_lsn
        ]

        status = {}

        for record in records:
            tid = record["tid"]

            if record["op"] == "BEGIN":
                status[tid] = "ACTIVE"
            elif record["op"] == "COMMIT":
                status[tid] = "COMMITTED"

        losers = {
            tid for tid, state in status.items()
            if state == "ACTIVE"
        }

        print("--- REDO ---")
        for record in records:
            if record["op"] == "WRITE":
                self.disk[record["item"]] = record["new"]
                print(
                    f"REDO {record['tid']}: "
                    f"{record['item']} = {record['new']} "
                    f"(LSN {record['lsn']})"
                )

        print("--- UNDO ---")
        for record in reversed(records):
            if (
                record["op"] == "WRITE"
                and record["tid"] in losers
            ):
                item = record["item"]
                new = record["new"]
                old = record["old"]
                self.disk[item] = old
                print(
                    f"UNDO {record['tid']}: "
                    f"{item}: {new} -> {old}"
                )

        self.buffer = self.disk.copy()
        print(f"\nRecovered database: {self.disk}")


db = DatabaseCheckpointSimulator()

print("Initial database:", db.disk)

db.begin("T1")
db.write("T1", "A", 150)
db.flush_page("A")
db.commit("T1")

db.checkpoint()

print()
db.begin("T2")
db.write("T2", "B", 250)
db.flush_page("B")

db.crash()
db.recover()
