# Bloom Filter for Database Membership Testing

class BloomFilter:
    def __init__(self, size=100, hash_count=3):
        self.size = size
        self.hash_count = hash_count
        self.bits = [0] * size

    def _hashes(self, key):
        key = str(key)

        h1 = hash(key)
        h2 = hash(key + "salt")

        for i in range(self.hash_count):
            yield (h1 + i * h2 + i * i) % self.size

    def add(self, key):
        for index in self._hashes(key):
            self.bits[index] = 1

    def might_contain(self, key):
        for index in self._hashes(key):
            if self.bits[index] == 0:
                return False

        return True


class DatabaseIndex:
    def __init__(self):
        self.bloom = BloomFilter(1000, 5)
        self.data = {}

    def insert(self, key, value):
        self.data[key] = value
        self.bloom.add(key)

    def contains(self, key):
        if not self.bloom.might_contain(key):
            return False

        return key in self.data

    def get(self, key):
        if not self.bloom.might_contain(key):
            return None

        return self.data.get(key)


db = DatabaseIndex()

db.insert(101, "Rahul")
db.insert(102, "Aman")
db.insert(103, "Vikas")
db.insert(104, "Arjun")

print(db.contains(101))
print(db.contains(999))

print(db.get(102))
print(db.get(999))feat: implement bloom filter for database membership testing