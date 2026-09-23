# Database Buffer Pool with Clock Replacement

class Page:
    def __init__(self, page_id):
        self.page_id = page_id
        self.data = None
        self.dirty = False
        self.reference = 0
        self.pin_count = 0


class ClockBufferPool:
    def __init__(self, capacity):
        self.capacity = capacity
        self.frames = [None] * capacity
        self.hand = 0
        self.page_table = {}

    def access_page(self, page_id):
        if page_id in self.page_table:
            page = self.page_table[page_id]
            page.reference = 1
            page.pin_count += 1

            print(f"Page {page_id}: BUFFER HIT")
            return page

        print(f"Page {page_id}: BUFFER MISS")

        frame = self.find_victim()

        if frame is None:
            print("No replaceable frame available")
            return None

        old_page = self.frames[frame]

        if old_page is not None:
            if old_page.dirty:
                self.flush_page(old_page)

            del self.page_table[old_page.page_id]

        page = Page(page_id)
        page.reference = 1
        page.pin_count = 1

        self.frames[frame] = page
        self.page_table[page_id] = page

        print(f"Page {page_id}: loaded into frame {frame}")

        return page

    def find_victim(self):
        checked = 0

        while checked < self.capacity * 2:
            page = self.frames[self.hand]

            if page is None:
                frame = self.hand
                self.hand = (
                    self.hand + 1
                ) % self.capacity
                return frame

            if page.pin_count > 0:
                self.hand = (
                    self.hand + 1
                ) % self.capacity
                checked += 1
                continue

            if page.reference == 1:
                page.reference = 0
                self.hand = (
                    self.hand + 1
                ) % self.capacity
                checked += 1
                continue

            frame = self.hand

            self.hand = (
                self.hand + 1
            ) % self.capacity

            return frame

        return None

    def unpin(self, page_id, dirty=False):
        if page_id not in self.page_table:
            return

        page = self.page_table[page_id]

        if page.pin_count > 0:
            page.pin_count -= 1

        if dirty:
            page.dirty = True

    def flush_page(self, page):
        print(f"Writing dirty page {page.page_id} to disk")
        page.dirty = False

    def flush_all(self):
        for page in self.frames:
            if page is not None and page.dirty:
                self.flush_page(page)

    def show(self):
        print("\nBuffer Pool:")

        for i, page in enumerate(self.frames):
            if page is None:
                print(f"Frame {i}: EMPTY")
            else:
                print(
                    f"Frame {i}: "
                    f"Page={page.page_id}, "
                    f"Ref={page.reference}, "
                    f"Pin={page.pin_count}, "
                    f"Dirty={page.dirty}"
                )


buffer = ClockBufferPool(3)

buffer.access_page(1)
buffer.unpin(1)

buffer.access_page(2)
buffer.unpin(2, dirty=True)

buffer.access_page(3)
buffer.unpin(3)

buffer.show()

buffer.access_page(1)
buffer.unpin(1)

buffer.access_page(4)
buffer.unpin(4)

buffer.show()

buffer.flush_all()