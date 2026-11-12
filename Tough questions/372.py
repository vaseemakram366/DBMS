# Dirty Page Management in Buffer Pool


class BufferManager:
    def __init__(self, disk):
        self.disk = disk
        self.buffer = {}

    def load_page(self, page):
        self.buffer[page] = {
            "data": self.disk[page],
            "dirty": False
        }
        print(f"Page {page} loaded into buffer")

    def update_page(self, page, new_data):
        self.buffer[page]["data"] = new_data
        self.buffer[page]["dirty"] = True
        print(f"Page {page} updated in buffer (dirty)")

    def flush_all(self):
        for page, info in self.buffer.items():
            if info["dirty"]:
                self.disk[page] = info["data"]
                info["dirty"] = False
                print(f"Page {page} written to disk (clean)")


disk = {1: "A", 2: "B"}

manager = BufferManager(disk)

manager.load_page(1)
manager.load_page(2)

manager.update_page(1, "A1")
manager.update_page(2, "B1")

manager.flush_all()

print("Disk data:", disk)

dirty_pages = [
    page for page, info in manager.buffer.items()
    if info["dirty"]
]

print("Dirty pages:", dirty_pages)
