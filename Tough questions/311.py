# Lock Escalation Simulator


class LockEscalation:
    def __init__(self, threshold=3):
        self.threshold = threshold
        self.record_locks = {}
        self.table_locks = set()

    def acquire_record_lock(self, transaction, record):
        if transaction in self.table_locks:
            print(f"{transaction} already has table lock")
            return

        self.record_locks.setdefault(transaction, set())
        self.record_locks[transaction].add(record)

        print(f"{transaction} locked {record}")

        if len(self.record_locks[transaction]) >= self.threshold:
            self.escalate(transaction)

    def escalate(self, transaction):
        self.record_locks[transaction].clear()
        self.table_locks.add(transaction)

        print(f"{transaction}: Lock escalation completed")
        print(f"{transaction}: Record locks converted to table lock")

    def show_status(self):
        print("Table Locks:", sorted(self.table_locks))
        print("Record Locks:", self.record_locks)


db = LockEscalation(threshold=3)

db.acquire_record_lock("T1", "R1")
db.acquire_record_lock("T1", "R2")
db.acquire_record_lock("T1", "R3")

db.show_status()
