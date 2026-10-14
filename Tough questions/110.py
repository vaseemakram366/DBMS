# Database Storage Fragmentation Analyzer


class StorageFragmentationAnalyzer:
    def __init__(self, page_size):
        if page_size <= 0:
            raise ValueError("Page size must be positive")

        self.page_size = page_size
        self.pages = {}

    def add_page(self, page_id, free_blocks):
        if any(size < 0 for size in free_blocks):
            raise ValueError("Free block sizes cannot be negative")

        if sum(free_blocks) > self.page_size:
            raise ValueError("Free space exceeds page size")

        self.pages[page_id] = free_blocks[:]

    def analyze_page(self, page_id):
        if page_id not in self.pages:
            raise ValueError("Page not found")

        free_blocks = self.pages[page_id]
        total_free = sum(free_blocks)
        used_space = self.page_size - total_free
        largest_block = max(free_blocks, default=0)

        fragmentation = 0
        if total_free > 0:
            fragmentation = (
                (total_free - largest_block) / total_free
            ) * 100

        return {
            "page_id": page_id,
            "used": used_space,
            "free": total_free,
            "largest_block": largest_block,
            "fragmentation": fragmentation
        }

    def report(self):
        print("===== Storage Fragmentation Report =====")

        total_used = 0
        total_free = 0

        for page_id in self.pages:
            result = self.analyze_page(page_id)
            total_used += result["used"]
            total_free += result["free"]

            print(f"\nPage {result['page_id']}:")
            print(f"  Used space: {result['used']} bytes")
            print(f"  Free space: {result['free']} bytes")
            print(
                f"  Largest free block: "
                f"{result['largest_block']} bytes"
            )
            print(
                f"  Fragmentation: "
                f"{result['fragmentation']:.2f}%"
            )

        total_capacity = len(self.pages) * self.page_size
        utilization = (
            total_used / total_capacity * 100
            if total_capacity else 0
        )

        print("\n===== Overall Statistics =====")
        print(f"Total capacity: {total_capacity} bytes")
        print(f"Total used: {total_used} bytes")
        print(f"Total free: {total_free} bytes")
        print(f"Space utilization: {utilization:.2f}%")


analyzer = StorageFragmentationAnalyzer(page_size=1000)

analyzer.add_page(1, [100, 50, 200])
analyzer.add_page(2, [300])
analyzer.add_page(3, [50, 50, 50, 50])

analyzer.report()
