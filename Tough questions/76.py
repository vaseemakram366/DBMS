# Database WAL Log Sequence Number (LSN) Manager

class LogRecord:
    def __init__(self, lsn, transaction_id, page_id, operation, old_value, new_value):
        self.lsn = lsn
        self.transaction_id = transaction_id
        self.page_id = page_id
        self.operation = operation
        self.old_value = old_value
        self.new_value = new_value

    def __repr__(self):
        return (
            f"LSN={self.lsn}, "
            f"TXN={self.transaction_id}, "
            f"PAGE={self.page_id}, "
            f"OP={self.operation}"
        )


class WALManager:
    def __init__(self):
        self.next_lsn = 1
        self.log = []

    def append(self, transaction_id, page_id,
               operation, old_value, new_value):

        record = LogRecord(
            self.next_lsn,
            transaction_id,
            page_id,
            operation,
            old_value,
            new_value
        )

        self.log.append(record)

        self.next_lsn += 1

        return record.lsn

    def get_logs(self):
        return self.log


class Page:
    def __init__(self, page_id, value):
        self.page_id = page_id
        self.value = value
        self.page_lsn = 0

    def __repr__(self):
        return (
            f"Page={self.page_id}, "
            f"Value={self.value}, "
            f"PageLSN={self.page_lsn}"
        )


class Database:
    def __init__(self):
        self.pages = {}
        self.wal = WALManager()

    def create_page(self, page_id, value):
        self.pages[page_id] = Page(
            page_id,
            value
        )

    def update(self, transaction_id, page_id, new_value):
        page = self.pages[page_id]

        old_value = page.value

        lsn = self.wal.append(
            transaction_id,
            page_id,
            "UPDATE",
            old_value,
            new_value
        )

        page.value = new_value
        page.page_lsn = lsn

        return lsn

    def redo(self, log_record):
        page = self.pages[log_record.page_id]

        if log_record.lsn > page.page_lsn:
            page.value = log_record.new_value
            page.page_lsn = log_record.lsn

    def recover(self):
        for record in self.wal.get_logs():
            self.redo(record)

    def display(self):
        for page in self.pages.values():
            print(page)


db = Database()

db.create_page(1, 100)
db.create_page(2, 200)

lsn1 = db.update(101, 1, 150)
lsn2 = db.update(102, 2, 250)
lsn3 = db.update(101, 1, 175)

print("LSNs:")
print(lsn1, lsn2, lsn3)

print("\nWAL:")
for record in db.wal.get_logs():
    print(record)

print("\nPages:")
db.display()

print("\nRecovery:")
db.recover()

db.display()