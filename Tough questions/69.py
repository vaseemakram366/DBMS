# Database Page Cache with Pin/Unpin

class BufferFrame:
    def __init__(self, page_id, data):
        self.page_id = page_id
        self.data = data
        self.pin_count = 0
        self.dirty = False


class PageCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.frames = {}

    def fetch_page(self, page_id, data=None):
        if page_id in self.frames:
            frame = self.frames[page_id]
            frame.pin_count += 1
            return frame

        if len(self.frames) >= self.capacity:
            if not self.evict_page():
                raise MemoryError("No unpinned page available")

        frame = BufferFrame(page_id, data)
        frame.pin_count = 1

        self.frames[page_id] = frame

        return frame

    def unpin_page(self, page_id, dirty=False):
        if page_id not in self.frames:
            return False

        frame = self.frames[page_id]

        if frame.pin_count > 0:
            frame.pin_count -= 1

        if dirty:
            frame.dirty = True

        return True

    def evict_page(self):
        for page_id, frame in list(self.frames.items()):
            if frame.pin_count == 0:
                if frame.dirty:
                    print(f"Writing dirty page {page_id} to disk")

                del self.frames[page_id]

                print(f"Evicted page {page_id}")

                return True

        return False

    def mark_dirty(self, page_id):
        if page_id in self.frames:
            self.frames[page_id].dirty = True

    def display(self):
        print("\nBuffer Pool:")

        for page_id, frame in self.frames.items():
            print(
                f"Page {page_id} | "
                f"Pin Count: {frame.pin_count} | "
                f"Dirty: {frame.dirty}"
            )


cache = PageCache(3)

cache.fetch_page(1, "Employee Data")
cache.fetch_page(2, "Department Data")
cache.fetch_page(3, "Salary Data")

cache.display()

cache.unpin_page(1)

cache.mark_dirty(2)

cache.display()

cache.fetch_page(4, "Project Data")

cache.display()

cache.unpin_page(2)
cache.unpin_page(3)

cache.fetch_page(5, "Location Data")

cache.display()