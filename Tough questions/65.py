# Free Space Map (FSM) — Database Page Allocation

class FreeSpaceMap:
    def __init__(self):
        self.pages = {}

    def add_page(self, page_id, free_space):
        self.pages[page_id] = free_space

    def update_space(self, page_id, free_space):
        if page_id in self.pages:
            self.pages[page_id] = free_space

    def find_page(self, required_space):
        candidates = []

        for page_id, free_space in self.pages.items():
            if free_space >= required_space:
                candidates.append((free_space, page_id))

        if not candidates:
            return None

        candidates.sort()

        return candidates[0][1]

    def remove_page(self, page_id):
        if page_id in self.pages:
            del self.pages[page_id]

    def display(self):
        print("Free Space Map")

        for page_id, free_space in sorted(self.pages.items()):
            print(
                f"Page {page_id}: "
                f"{free_space} bytes free"
            )


class DatabaseStorage:
    def __init__(self):
        self.fsm = FreeSpaceMap()
        self.pages = {}

    def create_page(self, page_id, page_size):
        self.pages[page_id] = page_size
        self.fsm.add_page(page_id, page_size)

    def insert(self, record_size):
        page_id = self.fsm.find_page(record_size)

        if page_id is None:
            page_id = len(self.pages)

            page_size = 256

            self.pages[page_id] = page_size
            self.fsm.add_page(page_id, page_size)

        self.pages[page_id] -= record_size

        self.fsm.update_space(
            page_id,
            self.pages[page_id]
        )

        return page_id

    def delete(self, page_id, freed_space):
        if page_id not in self.pages:
            return False

        self.pages[page_id] += freed_space

        self.fsm.update_space(
            page_id,
            self.pages[page_id]
        )

        return True

    def display(self):
        self.fsm.display()


db = DatabaseStorage()

db.create_page(0, 256)
db.create_page(1, 256)
db.create_page(2, 256)

print("Inserted into page:", db.insert(100))
print("Inserted into page:", db.insert(80))
print("Inserted into page:", db.insert(50))
print("Inserted into page:", db.insert(120))

db.display()

print("\nAfter deleting 50 bytes from Page 0:")

db.delete(0, 50)

db.display()