# Database Heap File Manager

class HeapPage:
    def __init__(self, page_id, capacity):
        self.page_id = page_id
        self.capacity = capacity
        self.records = []

    def has_space(self):
        return len(self.records) < self.capacity

    def insert(self, record):
        if not self.has_space():
            return None

        slot_id = len(self.records)
        self.records.append(record)

        return slot_id

    def read(self, slot_id):
        if slot_id >= len(self.records):
            return None

        return self.records[slot_id]

    def delete(self, slot_id):
        if slot_id >= len(self.records):
            return False

        self.records[slot_id] = None
        return True


class HeapFile:
    def __init__(self, page_capacity=3):
        self.page_capacity = page_capacity
        self.pages = []

    def create_page(self):
        page_id = len(self.pages)

        page = HeapPage(
            page_id,
            self.page_capacity
        )

        self.pages.append(page)

        return page

    def insert(self, record):
        for page in self.pages:
            if page.has_space():
                slot_id = page.insert(record)
                return page.page_id, slot_id

        page = self.create_page()

        slot_id = page.insert(record)

        return page.page_id, slot_id

    def read(self, page_id, slot_id):
        if page_id >= len(self.pages):
            return None

        return self.pages[page_id].read(slot_id)

    def delete(self, page_id, slot_id):
        if page_id >= len(self.pages):
            return False

        return self.pages[page_id].delete(slot_id)

    def scan(self):
        for page in self.pages:
            for slot_id, record in enumerate(page.records):
                if record is not None:
                    yield page.page_id, slot_id, record

    def display(self):
        for page in self.pages:
            print(
                f"Page {page.page_id}: "
                f"{page.records}"
            )


heap = HeapFile(page_capacity=3)

records = [
    {"id": 1, "name": "Aman"},
    {"id": 2, "name": "Rahul"},
    {"id": 3, "name": "Priya"},
    {"id": 4, "name": "Neha"},
    {"id": 5, "name": "Ravi"},
    {"id": 6, "name": "Anjali"},
    {"id": 7, "name": "Karan"}
]

for record in records:
    location = heap.insert(record)
    print(
        f"Inserted {record['name']} "
        f"at Page {location[0]}, Slot {location[1]}"
    )

print("\nHeap File:")
heap.display()

print("\nRead:")
print(heap.read(1, 1))

print("\nDelete:")
heap.delete(0, 1)

heap.display()

print("\nSequential Scan:")

for page_id, slot_id, record in heap.scan():
    print(
        f"Page={page_id}, "
        f"Slot={slot_id}, "
        f"Record={record}"
    )