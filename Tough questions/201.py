# Database Transaction Isolation Levels Simulator


class IsolationSimulator:
    def __init__(self, initial_value):
        self.committed_value = initial_value
        self.pending_value = None
        self.t1_active = False

    def begin_t1(self):
        self.t1_active = True
        self.pending_value = None
        print("T1 started")

    def write_t1(self, value):
        self.pending_value = value
        print(f"T1 writes uncommitted value = {value}")

    def read_t2(self, isolation_level):
        if isolation_level == "READ UNCOMMITTED":
            if self.pending_value is not None:
                value = self.pending_value
            else:
                value = self.committed_value
        else:
            value = self.committed_value

        print(f"T2 reads {value} ({isolation_level})")
        return value

    def commit_t1(self):
        if self.pending_value is not None:
            self.committed_value = self.pending_value

        self.pending_value = None
        self.t1_active = False
        print(f"T1 committed: database value = {self.committed_value}")

    def rollback_t1(self):
        self.pending_value = None
        self.t1_active = False
        print(f"T1 rolled back: database value = {self.committed_value}")


db = IsolationSimulator(100)

db.begin_t1()
db.write_t1(200)

db.read_t2("READ UNCOMMITTED")
db.read_t2("READ COMMITTED")

db.rollback_t1()

db.read_t2("READ COMMITTED")
