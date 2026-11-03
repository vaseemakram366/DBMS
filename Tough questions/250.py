# Database Page Corruption Detection


import hashlib


class DatabaseChecker:
    def __init__(self):
        self.pages = {}
        self.checksums = {}

    def checksum(self, data):
        return hashlib.sha256(data.encode()).hexdigest()

    def add_page(self, page_id, data):
        self.pages[page_id] = data
        self.checksums[page_id] = self.checksum(data)

    def corrupt_page(self, page_id, new_data):
        self.pages[page_id] = new_data

    def detect_corruption(self):
        for page_id, data in self.pages.items():
            current = self.checksum(data)
            expected = self.checksums[page_id]

            if current != expected:
                print(f"Page {page_id}: CORRUPTED")
            else:
                print(f"Page {page_id}: OK")


db = DatabaseChecker()

db.add_page(1, "Student A")
db.add_page(2, "Student B")
db.add_page(3, "Student C")

db.corrupt_page(2, "Unknown Data")

db.detect_corruption()
