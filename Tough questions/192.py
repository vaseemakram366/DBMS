# Strict Two-Phase Locking (Strict 2PL) Simulator


class Strict2PLSimulator:
    def __init__(self):
        self.database = {"A": 100, "B": 200}
        self.locks = {}
        self.transaction_locks = {}
        self.undo_logs = {}
        self.active = set()

    def begin(self, tid):
        if tid in self.active:
            print(f"{tid} is already active")
            return

        self.active.add(tid)
        self.transaction_locks[tid] = set()
        self.undo_logs[tid] = {}
        print(f"{tid} started")

    def acquire_lock(self, tid, item):
        if tid not in self.active:
            print(f"{tid}: transaction is not active")
            return False

        owner = self.locks.get(item)

        if owner is not None and owner != tid:
            print(f"{tid} must wait: {item} is locked by {owner}")
            return False

        self.locks[item] = tid
        self.transaction_locks[tid].add(item)
        print(f"{tid} acquired exclusive lock on {item}")
        return True

    def write(self, tid, item, value):
        if tid not in self.active:
            print(f"{tid}: transaction is not active")
            return False

        if self.locks.get(item) != tid:
            print(f"{tid}: cannot write {item} without its lock")
            return False

        if item not in self.undo_logs[tid]:
            self.undo_logs[tid][item] = self.database[item]

        old = self.database[item]
        self.database[item] = value
        print(f"{tid} updated {item}: {old} -> {value}")
        return True

    def finish(self, tid, commit=True):
        if tid not in self.active:
            print(f"{tid}: transaction is not active")
            return

        if commit:
            print(f"{tid} committed")
        else:
            for item, old_value in self.undo_logs[tid].items():
                self.database[item] = old_value
            print(f"{tid} aborted; changes undone")

        for item in self.transaction_locks[tid]:
            if self.locks.get(item) == tid:
                del self.locks[item]

        del self.transaction_locks[tid]
        del self.undo_logs[tid]
        self.active.remove(tid)
        print(f"{tid} released all locks")

    def show_database(self):
        print("Database:", self.database)


db = Strict2PLSimulator()

db.begin("T1")
db.acquire_lock("T1", "A")
db.write("T1", "A", 150)

db.begin("T2")
db.acquire_lock("T2", "A")

db.finish("T1", commit=True)

db.acquire_lock("T2", "A")
db.write("T2", "A", 180)
db.finish("T2", commit=True)

db.show_database()
