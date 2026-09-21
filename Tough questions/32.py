# Multi-Version Concurrency Control

class Version:
    def __init__(self, value, transaction_id, commit_id):
        self.value = value
        self.transaction_id = transaction_id
        self.commit_id = commit_id


class MVCCDatabase:
    def __init__(self):
        self.data = {}
        self.next_transaction_id = 1
        self.next_commit_id = 1

    def begin(self):
        transaction_id = self.next_transaction_id
        self.next_transaction_id += 1

        snapshot = self.next_commit_id - 1

        return Transaction(
            transaction_id,
            snapshot,
            self
        )

    def read_version(self, key, snapshot):
        if key not in self.data:
            return None

        versions = self.data[key]

        visible = None

        for version in versions:
            if version.commit_id <= snapshot:
                visible = version

        return visible


class Transaction:
    def __init__(self, transaction_id, snapshot, database):
        self.transaction_id = transaction_id
        self.snapshot = snapshot
        self.database = database
        self.writes = {}

    def read(self, key):
        if key in self.writes:
            return self.writes[key]

        version = self.database.read_version(
            key,
            self.snapshot
        )

        if version is None:
            return None

        return version.value

    def write(self, key, value):
        self.writes[key] = value

    def commit(self):
        for key, value in self.writes.items():
            commit_id = self.database.next_commit_id
            self.database.next_commit_id += 1

            version = Version(
                value,
                self.transaction_id,
                commit_id
            )

            if key not in self.database.data:
                self.database.data[key] = []

            self.database.data[key].append(version)

        print(
            f"T{self.transaction_id} committed"
        )


db = MVCCDatabase()

t1 = db.begin()

t1.write("balance", 1000)
t1.commit()

t2 = db.begin()

print("T2 reads:", t2.read("balance"))

t3 = db.begin()

t3.write("balance", 2000)
t3.commit()

print("T2 reads again:", t2.read("balance"))

t4 = db.begin()

print("T4 reads:", t4.read("balance"))