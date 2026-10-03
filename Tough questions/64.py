# Slotted Page Storage Manager

class SlottedPage:
    def __init__(self, page_size=256):
        self.page_size = page_size
        self.data = bytearray(page_size)
        self.slots = {}
        self.free_start = 0
        self.next_slot = 0

    def insert(self, record):
        record = record.encode()
        size = len(record)

        if self.free_start + size > self.page_size:
            raise MemoryError("Page is full")

        slot_id = self.next_slot

        self.data[self.free_start:self.free_start + size] = record

        self.slots[slot_id] = (
            self.free_start,
            size
        )

        self.free_start += size
        self.next_slot += 1

        return slot_id

    def read(self, slot_id):
        if slot_id not in self.slots:
            return None

        offset, size = self.slots[slot_id]

        record = self.data[offset:offset + size]

        return record.decode()

    def delete(self, slot_id):
        if slot_id not in self.slots:
            return False

        del self.slots[slot_id]
        return True

    def update(self, slot_id, record):
        if slot_id not in self.slots:
            return False

        old_offset, old_size = self.slots[slot_id]
        new_record = record.encode()
        new_size = len(new_record)

        if new_size <= old_size:
            self.data[
                old_offset:old_offset + new_size
            ] = new_record

            self.slots[slot_id] = (
                old_offset,
                new_size
            )

            return True

        if self.free_start + new_size > self.page_size:
            return False

        self.data[
            self.free_start:self.free_start + new_size
        ] = new_record

        self.slots[slot_id] = (
            self.free_start,
            new_size
        )

        self.free_start += new_size

        return True

    def display(self):
        print("Page Size:", self.page_size)
        print("Slots:", self.slots)
        print("Free Space:", self.page_size - self.free_start)


page = SlottedPage()

s1 = page.insert("Aman,20,CSE")
s2 = page.insert("Rahul,21,IT")
s3 = page.insert("Priya,20,AI")

print("Slot IDs:", s1, s2, s3)

print(page.read(s1))
print(page.read(s2))
print(page.read(s3))

page.update(s2, "Rahul,22,CSE")

print(page.read(s2))

page.delete(s1)

print(page.read(s1))

page.display()