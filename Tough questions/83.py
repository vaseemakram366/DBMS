# Add Jack nested if compilation test

import hashlib


class CuckooFilter:
    def __init__(self, bucket_count=32, bucket_size=4, max_kicks=50):
        self.bucket_count = bucket_count
        self.bucket_size = bucket_size
        self.max_kicks = max_kicks
        self.buckets = [[] for _ in range(bucket_count)]

    def _hash(self, value):
        return int(
            hashlib.sha256(str(value).encode()).hexdigest(),
            16
        )

    def _fingerprint(self, value):
        return self._hash(value) & 0xFFFF

    def _index1(self, value):
        return self._hash(value) % self.bucket_count

    def _index2(self, index, fingerprint):
        return (
            index ^
            (hash(fingerprint) % self.bucket_count)
        ) % self.bucket_count

    def insert(self, value):
        fingerprint = self._fingerprint(value)

        i1 = self._index1(value)
        i2 = self._index2(i1, fingerprint)

        if len(self.buckets[i1]) < self.bucket_size:
            self.buckets[i1].append(fingerprint)
            return True

        if len(self.buckets[i2]) < self.bucket_size:
            self.buckets[i2].append(fingerprint)
            return True

        index = i1
        current = fingerprint

        for _ in range(self.max_kicks):
            position = hash(current) % self.bucket_size

            self.buckets[index][position], current = (
                current,
                self.buckets[index][position]
            )

            index = self._index2(index, current)

            if len(self.buckets[index]) < self.bucket_size:
                self.buckets[index].append(current)
                return True

        return False

    def contains(self, value):
        fingerprint = self._fingerprint(value)

        i1 = self._index1(value)
        i2 = self._index2(i1, fingerprint)

        return (
            fingerprint in self.buckets[i1]
            or fingerprint in self.buckets[i2]
        )

    def delete(self, value):
        fingerprint = self._fingerprint(value)

        i1 = self._index1(value)
        i2 = self._index2(i1, fingerprint)

        if fingerprint in self.buckets[i1]:
            self.buckets[i1].remove(fingerprint)
            return True

        if fingerprint in self.buckets[i2]:
            self.buckets[i2].remove(fingerprint)
            return True

        return False


class DatabaseIndex:
    def __init__(self):
        self.filter = CuckooFilter()

    def insert(self, key):
        return self.filter.insert(key)

    def contains(self, key):
        return self.filter.contains(key)

    def delete(self, key):
        return self.filter.delete(key)


db = DatabaseIndex()

db.insert(101)
db.insert(102)
db.insert(103)

print(db.contains(101))
print(db.contains(999))

db.delete(101)

print(db.contains(101))