# ARIES Recovery Simulator


class ARIESSimulator:
    def __init__(self, initial_data):
        self.disk = initial_data.copy()
        self.buffer = initial_data.copy()
        self.log = []
        self.active = set()
        self.committed = set()

    def append_log(self, op, tid, item=None, old=None, new=None):
        lsn = len(self.log) + 1
        record = {
            "lsn": lsn,
            "op": op,
            "tid": tid,
            "item": item,
            "old": old,
            "new": new,
        }
        self.log.append(record)
        return lsn

    def begin(self, tid):
        if tid in self.active or tid in self.committed:
            raise ValueError(f"T{tid} already exists")

        self.append_log("BEGIN", tid)
        self.active.add(tid)
        print(f"T{tid} BEGIN")

    def write(self, tid, item, value):
        if tid not in self.active:
            raise ValueError(f"T{tid} is not active")

        old = self.buffer[item]
        lsn = self.append_log("WRITE", tid, item, old, value)

        self.buffer[item] = value
        print(f"T{tid} WRITE {item}: {old} -> {value} (LSN {lsn})")

    def flush_page(self, item):
        # The corresponding log is already durable in this simulation.
        self.disk[item] = self.buffer[item]
        print(f"FLUSH {item} = {self.disk[item]}")

    def commit(self, tid):
        if tid not in self.active:
            raise ValueError(f"T{tid} is not active")

        self.append_log("COMMIT", tid)
        self.active.remove(tid)
        self.committed.add(tid)
        print(f"T{tid} COMMIT")

    def crash(self):
        print("\n*** CRASH ***")
        self.buffer = self.disk.copy()
        self.active.clear()
        self.committed.clear()
        print("Disk before recovery:", self.disk)

    def recover(self):
        print("\n--- PHASE 1: ANALYSIS ---")

        status = {}

        for record in self.log:
            tid = record["tid"]
            op = record["op"]

            if op == "BEGIN":
                status[tid] = "ACTIVE"
            elif op == "COMMIT":
                status[tid] = "COMMITTED"
            elif op == "END":
                status[tid] = "ENDED"
            elif op == "ABORT":
                status[tid] = "ABORTING"

        losers = {
            tid for tid, state in status.items()
            if state in ("ACTIVE", "ABORTING")
        }

        print("Transaction status:", status)
        print("Loser transactions:", sorted(losers))

        print("\n--- PHASE 2: REDO ---")

        # Replay history, including compensation log records.
        for record in self.log:
            if record["op"] in ("WRITE", "CLR"):
                item = record["item"]
                value = record["new"]
                self.disk[item] = value

                print(
                    f"LSN {record['lsn']}: "
                    f"{record['op']} {item} = {value}"
                )

        print("\n--- PHASE 3: UNDO ---")

        # Educational single-recovery-pass implementation.
        for tid in sorted(losers):
            writes = [
                record for record in self.log
                if record["tid"] == tid
                and record["op"] == "WRITE"
            ]

            for record in reversed(writes):
                item = record["item"]
                old = record["old"]
                current = self.disk[item]

                # CLR records the compensation before applying it.
                lsn = self.append_log(
                    "CLR", tid, item, current, old
                )
                self.disk[item] = old

                print(
                    f"T{tid}: UNDO {item}: "
                    f"{current} -> {old} (CLR LSN {lsn})"
                )

            self.append_log("END", tid)
            print(f"T{tid} END")

        # Transactions that committed are already complete.
        for tid, state in status.items():
            if state == "COMMITTED":
                self.append_log("END", tid)

        self.buffer = self.disk.copy()

        print("\nRecovered database:", self.disk)


def main():
    db = ARIESSimulator({"A": 100, "B": 200})

    print("Initial database:", db.disk)

    db.begin(1)
    db.write(1, "A", 150)
    db.flush_page("A")
    db.commit(1)

    db.begin(2)
    db.write(2, "B", 250)
    db.flush_page("B")

    db.crash()
    db.recover()


if __name__ == "__main__":
    main()
