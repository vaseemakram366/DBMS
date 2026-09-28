# Adaptive Hash Index

from collections import defaultdict


class AdaptiveHashIndex:
    def __init__(self, threshold=3):
        self.threshold = threshold
        self.access_count = defaultdict(int)
        self.hash_index = {}
        self.data = {}

    def insert(self, key, value):
        self.data[key] = value

        if key in self.hash_index:
            self.hash_index[key] = value

    def get(self, key):
        self.access_count[key] += 1

        if key in self.hash_index:
            print(f"AHI HIT: {key}")
            return self.hash_index[key]

        print(f"DATA LOOKUP: {key}")

        value = self.data.get(key)

        if (
            self.access_count[key] >= self.threshold
            and value is not None
        ):
            self.hash_index[key] = value
            print(f"AHI CREATED: {key}")

        return value

    def update(self, key, value):
        self.data[key] = value

        if key in self.hash_index:
            self.hash_index[key] = value

    def delete(self, key):
        self.data.pop(key, None)
        self.hash_index.pop(key, None)
        self.access_count.pop(key, None)

    def show(self):
        print("\nBase Data:")
        print(self.data)

        print("\nAdaptive Hash Index:")
        print(self.hash_index)

        print("\nAccess Counters:")
        print(dict(self.access_count))


db = AdaptiveHashIndex(threshold=3)

db.insert("user:101", "Amit")
db.insert("user:102", "Rahul")
db.insert("user:103", "Vaseem")
db.insert("user:104", "Neha")

print(db.get("user:101"))
print(db.get("user:101"))
print(db.get("user:101"))

print(db.get("user:101"))
print(db.get("user:101"))

db.update("user:101", "Amit Kumar")

print(db.get("user:101"))

db.delete("user:103")

db.show()