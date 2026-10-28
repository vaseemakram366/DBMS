# Write-Ahead Logging (WAL) Simulator


class WALSimulator:
    def __init__(self, initial_data):
        self.disk_pages = initial_data.copy()
        self.buffer = initial_data.copy()
        self.log = []
        self.active = set()
        self.locks = {}

    def append_log(self, record):
        # Simulate a durable log write to disk.
        self.log.append(record)
        return len(self.log)

    def begin(self, tid):
        if tid in self.active:
            raise ValueError(f"T{tid} is already active")

        self.append_log(("BEGIN", tid, None, None, None))
        self.active.add(tid)
        print(f"T{tid} BEGIN (log durable)")

    def write(self, tid, item, value):
        if tid not in self.active:
            raise ValueError(f"T{tid} is not active")

        owner = self.locks.get(item)
        if owner is not None and owner != tid:
            raise ValueError(f"{item} is locked by T{owner}")

        old_value = self.buffer[item]

        # WAL rule: record the change before a page is flushed.
        lsn = self.append_log(
            ("WRITE", tid, item, old_value, value)
        )

        self.locks[item] = tid
        self.buffer[item] = value

        print(
            f"T{tid} WRITE {item}: "
            f"{old_value} -> {value} (LSN {lsn})"
        )

    def flush_page(self, item):
        # All log records are already durable in this simulation.
        self.disk_pages[item] = self.buffer[item]
        print(f"FLUSH {item} = {self.disk_pages[item]} to disk")

    def commit(self, tid):
        if tid not in self.active:
            raise ValueError(f"T{tid} is not active")

        self.append_log(("COMMIT", tid, None, None, None))
        self.active.remove(tid)
        self._release_locks(tid)
        print(f"T{tid} COMMIT (commit log durable)")

    def _release_locks(self, tid):
        for item in list(self.locks):
            if self.locks[item] == tid:
                del self.locks[item]

    def crash(self):
        print("\n*** CRASH OCCURRED ***")
        print("Disk pages before recovery:", self.disk_pages)

        # Volatile state is lost.
        self.buffer = self.disk_pages.copy()
        self.active.clear()
        self.locks.clear()

    def recover(self):
        committed = {
            record[1]
            for record in self.log
            if record[0] == "COMMIT"
        }

        writes = [
            record for record in self.log
            if record[0] == "WRITE"
        ]

        print("\n--- REDO PHASE ---")
        for _, tid, item, old_value, new_value in writes:
            if tid in committed:
                self.disk_pages[item] = new_value
                print(f"REDO T{tid}: {item} = {new_value}")

        print("\n--- UNDO PHASE ---")
        for _, tid, item, old_value, new_value in reversed(writes):
            if tid not in committed:
                self.disk_pages[item] = old_value
                print(f"UNDO T{tid}: {item} = {old_value}")

        self.buffer = self.disk_pages.copy()
        print("\nRecovered database:", self.disk_pages)


def main():
    db = WALSimulator({"A": 100, "B": 200})

    print("Initial disk pages:", db.disk_pages)

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
