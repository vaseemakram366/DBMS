# LSM Tree — Log-Structured Merge Tree

import bisect


class SSTable:
    def __init__(self, data):
        self.data = sorted(data.items())
        self.keys = [key for key, _ in self.data]

    def get(self, key):
        index = bisect.bisect_left(self.keys, key)

        if index < len(self.keys):
            if self.keys[index] == key:
                return self.data[index][1]

        return None

    def items(self):
        return self.data


class LSMTree:
    def __init__(self, memtable_limit=4):
        self.memtable = {}
        self.sstables = []
        self.memtable_limit = memtable_limit

    def put(self, key, value):
        self.memtable[key] = value

        if len(self.memtable) >= self.memtable_limit:
            self.flush()

    def get(self, key):
        if key in self.memtable:
            return self.memtable[key]

        for sstable in reversed(self.sstables):
            value = sstable.get(key)

            if value is not None:
                return value

        return None

    def flush(self):
        if not self.memtable:
            return

        sstable = SSTable(self.memtable)

        self.sstables.append(sstable)

        self.memtable.clear()

        print("MemTable flushed to SSTable")

    def compact(self):
        if len(self.sstables) < 2:
            return

        merged = {}

        for sstable in self.sstables:
            for key, value in sstable.items():
                merged[key] = value

        self.sstables = [
            SSTable(merged)
        ]

        print("SSTables compacted")

    def delete(self, key):
        self.put(key, None)

    def show(self):
        print("\nMemTable:")
        print(self.memtable)

        print("\nSSTables:")

        for i, sstable in enumerate(self.sstables):
            print(i, sstable.items())


db = LSMTree(memtable_limit=3)

db.put("A", 100)
db.put("B", 200)
db.put("C", 300)

db.put("D", 400)
db.put("E", 500)

print("\nRead A:", db.get("A"))
print("Read D:", db.get("D"))
print("Read X:", db.get("X"))

db.put("A", 999)

print("\nUpdated A:", db.get("A"))

db.flush()

db.compact()

db.show()