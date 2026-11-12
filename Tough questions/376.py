# Free Page List Management


class FreePageManager:
    def __init__(self, total_pages):
        self.free_pages = list(range(total_pages))

    def allocate_page(self):
        if not self.free_pages:
            print("No free pages available")
            return -1

        page = self.free_pages.pop(0)
        print(f"Page {page} allocated")
        return page

    def release_page(self, page):
        if page not in self.free_pages:
            self.free_pages.append(page)
            print(f"Page {page} released")
        else:
            print(f"Page {page} is already free")

    def display(self):
        print("Free Pages:", self.free_pages)


manager = FreePageManager(5)

manager.allocate_page()
manager.allocate_page()

manager.release_page(0)

manager.display()
