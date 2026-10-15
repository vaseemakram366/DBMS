# Database Index Usage Analyzer


from dataclasses import dataclass


@dataclass
class IndexStats:
    name: str
    table: str
    reads: int = 0
    writes: int = 0
    size_mb: float = 0.0


class IndexUsageAnalyzer:
    def __init__(self):
        self.indexes = {}

    def register_index(self, name, table, size_mb):
        if size_mb < 0:
            raise ValueError("Index size cannot be negative")

        if name in self.indexes:
            raise ValueError("Index already registered")

        self.indexes[name] = IndexStats(
            name=name,
            table=table,
            size_mb=size_mb
        )

    def record_read(self, index_name, count=1):
        if index_name not in self.indexes:
            raise ValueError("Unknown index")
        if count < 0:
            raise ValueError("Count cannot be negative")

        self.indexes[index_name].reads += count

    def record_write(self, index_name, count=1):
        if index_name not in self.indexes:
            raise ValueError("Unknown index")
        if count < 0:
            raise ValueError("Count cannot be negative")

        self.indexes[index_name].writes += count

    def analyze(self):
        results = []

        for index in self.indexes.values():
            if index.reads == 0:
                status = "INVESTIGATE"
            elif index.reads >= 100:
                status = "HIGH USAGE"
            else:
                status = "LOW USAGE"

            results.append({
                "name": index.name,
                "table": index.table,
                "reads": index.reads,
                "writes": index.writes,
                "size_mb": index.size_mb,
                "status": status
            })

        return sorted(
            results,
            key=lambda item: (item["reads"], -item["size_mb"])
        )

    def report(self):
        print("===== Database Index Usage Report =====")

        results = self.analyze()

        if not results:
            print("No indexes registered.")
            return

        for item in results:
            print(f"\nIndex: {item['name']}")
            print(f"Table: {item['table']}")
            print(f"Read operations: {item['reads']}")
            print(f"Write operations: {item['writes']}")
            print(f"Size: {item['size_mb']:.2f} MB")
            print(f"Status: {item['status']}")

        total_size = sum(item["size_mb"] for item in results)
        total_reads = sum(item["reads"] for item in results)

        print("\n===== Summary =====")
        print(f"Total indexes: {len(results)}")
        print(f"Total index size: {total_size:.2f} MB")
        print(f"Total recorded reads: {total_reads}")


analyzer = IndexUsageAnalyzer()

analyzer.register_index("idx_users_email", "users", 25.0)
analyzer.register_index("idx_orders_date", "orders", 80.0)
analyzer.register_index("idx_products_name", "products", 40.0)

analyzer.record_read("idx_users_email", 1200)
analyzer.record_write("idx_users_email", 300)

analyzer.record_read("idx_orders_date", 35)
analyzer.record_write("idx_orders_date", 500)

analyzer.record_write("idx_products_name", 200)

analyzer.report()
