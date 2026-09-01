# Timestamp Ordering Protocol

class Database:
    def __init__(self):
        self.read_ts = {}
        self.write_ts = {}

    def initialize(self, item):
        self.read_ts[item] = 0
        self.write_ts[item] = 0

    def read(self, transaction, item, timestamp):
        if timestamp < self.write_ts[item]:
            print(
                transaction,
                "READ rejected on",
                item
            )
            return False

        self.read_ts[item] = max(
            self.read_ts[item],
            timestamp
        )

        print(
            transaction,
            "READ allowed on",
            item
        )

        return True

    def write(self, transaction, item, timestamp):
        if timestamp < self.read_ts[item]:
            print(
                transaction,
                "WRITE rejected on",
                item
            )
            return False

        if timestamp < self.write_ts[item]:
            print(
                transaction,
                "WRITE rejected on",
                item
            )
            return False

        self.write_ts[item] = timestamp

        print(
            transaction,
            "WRITE allowed on",
            item
        )

        return True


db = Database()

db.initialize("A")

db.read("T1", "A", 1)
db.write("T2", "A", 2)
db.read("T3", "A", 3)
db.write("T1", "A", 1)