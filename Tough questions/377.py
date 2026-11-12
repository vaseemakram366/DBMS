# Database Page Deallocation


class PageManager:
    def __init__(self, total_pages):
        self.allocated = set()

    def allocate(self, page):
        if page in self.allocated:
            print(f"Page {page} is already allocated")
        else:
            self.allocated.add(page)
            print(f"Page {page} allocated")

    def deallocate(self, page):
        if page in self.allocated:
            self.allocated.remove(page)
            print(f"Page {page} deallocated")
        else:
            print(f"Page {page} is not allocated")

    def display(self):
        print("Allocated Pages:", sorted(self.allocated))


manager = PageManager(5)

manager.allocate(1)
manager.allocate(2)
manager.allocate(3)

manager.deallocate(2)

manager.display()
