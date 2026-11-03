# Database Page Read/Write Simulator


class Database:
    def __init__(self):
        self.pages = {}

    def write_page(self, page_id, data):
        self.pages[page_id] = data
        print(f"Page {page_id} written successfully")

    def read_page(self, page_id):
        if page_id not in self.pages:
            print(f"Page {page_id} not found")
            return

        print(f"Page {page_id} data: {self.pages[page_id]}")

    def show_all_pages(self):
        print("All database pages:", self.pages)


db = Database()

db.write_page(1, "Student A")
db.write_page(2, "Student B")

db.read_page(1)

db.write_page(1, "Student A Updated")
db.read_page(1)

db.show_all_pages()
