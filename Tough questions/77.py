# Database Write-Ahead Log Logical Redo/Undo Engine

class LogRecord:
    def __init__(
        self,
        lsn,
        txn_id,
        page_id,
        old_value,
        new_value,
        operation
    ):
        self.lsn = lsn
        self.txn_id = txn_id
        self.page_id = page_id
        self.old_value = old_value
        self.new_value = new_value
        self.operation = operation

    def __repr__(self):
        return (
            f"LSN={self.lsn} "
            f"TXN={self.txn_id} "
            f"PAGE={self.page_id} "
            f"{self.old_value}->{self.new_value}"
        )


class WAL:
    def __init__(self):
        self.logs = []
        self.next_lsn = 1

    def write(
        self,
        txn_id,
        page_id,
        old_value,
        new_value,
        operation="UPDATE"
    ):
        record = LogRecord(
            self.next_lsn,
            txn_id,
            page_id,
            old_value,
            new_value,
            operation
        )

        self.logs.append(record)
        self.next_lsn += 1

        return record


class RecoveryManager:
    def __init__(self):
        self.wal = WAL()
        self.pages = {}
        self.transactions = {}

    def create_page(self, page_id, value):
        self.pages[page_id] = value

    def begin(self, txn_id):
        self.transactions[txn_id] = "ACTIVE"

    def update(self, txn_id, page_id, new_value):
        old_value = self.pages[page_id]

        record = self.wal.write(
            txn_id,
            page_id,
            old_value,
            new_value
        )

        self.pages[page_id] = new_value

        return record

    def commit(self, txn_id):
        self.transactions[txn_id] = "COMMITTED"

        self.wal.write(
            txn_id,
            -1,
            None,
            None,
            "COMMIT"
        )

    def crash(self):
        print("\n*** DATABASE CRASH ***")

    def recover(self):
        print("\nStarting Recovery...")

        committed = {
            txn_id
            for txn_id, state in self.transactions.items()
            if state == "COMMITTED"
        }

        active = {
            txn_id
            for txn_id, state in self.transactions.items()
            if state == "ACTIVE"
        }

        print("Committed Transactions:", committed)
        print("Uncommitted Transactions:", active)

        print("\nREDO Phase")

        for record in self.wal.logs:
            if (
                record.txn_id in committed
                and record.operation == "UPDATE"
            ):
                self.pages[record.page_id] = record.new_value

                print(
                    f"REDO LSN {record.lsn}: "
                    f"Page {record.page_id} = "
                    f"{record.new_value}"
                )

        print("\nUNDO Phase")

        for record in reversed(self.wal.logs):
            if (
                record.txn_id in active
                and record.operation == "UPDATE"
            ):
                self.pages[record.page_id] = record.old_value

                print(
                    f"UNDO LSN {record.lsn}: "
                    f"Page {record.page_id} = "
                    f"{record.old_value}"
                )

                self.transactions[
                    record.txn_id
                ] = "ABORTED"

    def display(self):
        print("\nDatabase Pages:")

        for page_id, value in self.pages.items():
            print(
                f"Page {page_id}: {value}"
            )


db = RecoveryManager()

db.create_page(1, 100)
db.create_page(2, 200)

db.begin(101)
db.update(101, 1, 150)
db.commit(101)

db.begin(102)
db.update(102, 2, 300)

db.display()

db.crash()

db.recover()

db.display()