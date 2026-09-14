# Extendible Hashing
class Bucket:
    def __init__(self, local_depth, capacity):
        self.local_depth = local_depth
        self.capacity = capacity
        self.keys = []

    def is_full(self):
        return len(self.keys) >= self.capacity


class ExtendibleHashing:
    def __init__(self, bucket_capacity=2):
        self.global_depth = 1
        self.bucket_capacity = bucket_capacity

        self.directory = [
            Bucket(1, bucket_capacity),
            Bucket(1, bucket_capacity)
        ]

    def _index(self, key):
        mask = (1 << self.global_depth) - 1
        return key & mask

    def insert(self, key):
        while True:
            index = self._index(key)
            bucket = self.directory[index]

            if key in bucket.keys:
                return

            if not bucket.is_full():
                bucket.keys.append(key)
                return

            self._split_bucket(index)

    def _split_bucket(self, index):
        old_bucket = self.directory[index]

        if old_bucket.local_depth == self.global_depth:
            self.directory += self.directory
            self.global_depth += 1

        new_depth = old_bucket.local_depth + 1

        new_bucket = Bucket(
            new_depth,
            self.bucket_capacity
        )

        old_bucket.local_depth = new_depth

        for i in range(len(self.directory)):
            if self.directory[i] is old_bucket:
                if ((i >> (new_depth - 1)) & 1) == 1:
                    self.directory[i] = new_bucket

        old_keys = old_bucket.keys[:]
        old_bucket.keys.clear()

        for key in old_keys:
            index = self._index(key)
            self.directory[index].keys.append(key)

    def search(self, key):
        index = self._index(key)

        if key in self.directory[index].keys:
            return True

        return False

    def display(self):
        print("\nGlobal Depth:", self.global_depth)

        for i, bucket in enumerate(self.directory):
            print(
                "Directory",
                i,
                "->",
                bucket.keys,
                "Local Depth:",
                bucket.local_depth
            )


db = ExtendibleHashing(2)

values = [1, 3, 5, 7, 9, 13, 17, 21]

for value in values:
    db.insert(value)

db.display()

print("\nSearch 13:", db.search(13))
print("Search 20:", db.search(20))