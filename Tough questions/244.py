# Dirty Page Tracking


class DirtyPageTracker:
    def __init__(self):
        self.pages = {}
        self.dirty_pages = set()

    def load_page(self, page_id, value):
        self.pages[page_id] = value
        print(f"Loaded page {page_id}")

    def modify_page(self, page_id, value):
        if page_id not in self.pages:
            print(f"Page {page_id} not in buffer")
            return

        self.pages[page_id] = value
        self.dirty_pages.add(page_id)
        print(f"Page {page_id} modified; marked dirty")

    def flush_page(self, page_id):
        if page_id in self.dirty_pages:
            self.dirty_pages.remove(page_id)
            print(f"Page {page_id} written to disk")
        else:
            print(f"Page {page_id} is clean")

    def show_dirty(self):
        print("Dirty pages:", sorted(self.dirty_pages))


tracker = DirtyPageTracker()

tracker.load_page(1, "A")
tracker.load_page(2, "B")

tracker.modify_page(1, "A*")
tracker.modify_page(2, "B*")

tracker.flush_page(1)
tracker.show_dirty()
