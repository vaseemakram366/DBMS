# Database Log-Structured Compaction Scheduler

class SSTable:
    def __init__(self, table_id, level, size):
        self.table_id = table_id
        self.level = level
        self.size = size

    def __repr__(self):
        return (
            f"SSTable(id={self.table_id}, "
            f"level={self.level}, "
            f"size={self.size})"
        )


class CompactionScheduler:
    def __init__(self, level_threshold=2, size_threshold=100):
        self.level_threshold = level_threshold
        self.size_threshold = size_threshold
        self.sstables = []

    def add_sstable(self, sstable):
        self.sstables.append(sstable)

    def should_compact(self, level):
        tables = [
            table
            for table in self.sstables
            if table.level == level
        ]

        if len(tables) >= self.level_threshold:
            return True

        total_size = sum(table.size for table in tables)

        return total_size >= self.size_threshold

    def select_compaction(self):
        levels = sorted(
            set(table.level for table in self.sstables)
        )

        for level in levels:
            if self.should_compact(level):
                candidates = [
                    table
                    for table in self.sstables
                    if table.level == level
                ]

                candidates.sort(key=lambda x: x.size)

                return candidates[:self.level_threshold]

        return []

    def compact(self):
        selected = self.select_compaction()

        if not selected:
            return None

        new_level = selected[0].level + 1

        new_size = sum(
            table.size
            for table in selected
        )

        new_id = max(
            table.table_id
            for table in self.sstables
        ) + 1

        for table in selected:
            self.sstables.remove(table)

        merged = SSTable(
            new_id,
            new_level,
            new_size
        )

        self.sstables.append(merged)

        return merged

    def display(self):
        for table in sorted(
            self.sstables,
            key=lambda x: (x.level, x.table_id)
        ):
            print(table)


scheduler = CompactionScheduler(
    level_threshold=2,
    size_threshold=100
)

scheduler.add_sstable(SSTable(1, 0, 40))
scheduler.add_sstable(SSTable(2, 0, 35))
scheduler.add_sstable(SSTable(3, 0, 30))
scheduler.add_sstable(SSTable(4, 1, 80))

print("Before Compaction:")
scheduler.display()

print("\nSelected for Compaction:")
print(scheduler.select_compaction())

merged = scheduler.compact()

print("\nCreated:")
print(merged)

print("\nAfter Compaction:")
scheduler.display()