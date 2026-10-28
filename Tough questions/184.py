# Transaction Recovery Simulator


class RecoverySimulator:
    def __init__(self, initial_data):
        self.database = initial_data.copy()
        self.undo_logs = {}
        self.committed = set()
        self.active = set()
        self.writer_locks = {}

    def begin(self, tid):
        if tid in self.active or tid in self.committed:
            raise ValueError(f"T{tid} already exists")

        self.active.add(tid)
        self.undo_logs[tid] = []
        print(f"T{tid} BEGIN")

    def write(self, tid, item, value):
        if tid not in self.active:
            raise ValueError(f"T{tid} is not active")

        owner = self.writer_locks.get(item)

        if owner is not None and owner != tid:
            raise ValueError(f"{item} is locked by T{owner}")

        old_value = self.database[item]
        self.undo_logs[tid].append((item, old_value))
        self.writer_locks[item] = tid
        self.database[item] = value

        print(
            f"T{tid} WRITE {item}: "
            f"{old_value} -> {value}"
        )

    def commit(self, tid):
        if tid not in self.active:
            raise ValueError(f"T{tid} is not active")

        self.active.remove(tid)
        self.committed.add(tid)
        self.undo_logs.pop(tid)

        self._release_locks(tid)
        print(f"T{tid} COMMIT")

    def abort(self, tid):
        if tid not in self.active:
            raise ValueError(f"T{tid} is not active")

        print(f"T{tid} ABORT")

        # Reverse the writes to restore old values.
        for item, old_value in reversed(self.undo_logs[tid]):
            current_value = self.database[item]
            self.database[item] = old_value

            print(
                f"  UNDO {item}: "
                f"{current_value} -> {old_value}"
            )

        self.active.remove(tid)
        self.undo_logs.pop(tid)
        self._release_locks(tid)

    def _release_locks(self, tid):
        for item in list(self.writer_locks):
            if self.writer_locks[item] == tid:
                del self.writer_locks[item]


def main():
    db = RecoverySimulator({"A": 100, "B": 200})

    print("Initial database:", db.database)

    db.begin(1)
    db.write(1, "A", 150)

    db.begin(2)
    db.write(2, "B", 250)

    db.commit(1)

    db.write(2, "A", 999)
    db.abort(2)

    print("\nFinal database:", db.database)
    print("Committed transactions:", sorted(db.committed))


if __name__ == "__main__":
    main()
