# Hash Index with Collision Handling


class HashIndex:
    def __init__(self, size=5):
        self.size = size
        self.buckets = [[] for _ in range(size)]

    def hash_key(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self.hash_key(key)
        bucket = self.buckets[index]

        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                print(f"Updated key {key} in bucket {index}")
                return

        if bucket:
            print(f"Collision for key {key} in bucket {index}")

        bucket.append((key, value))
        print(f"Inserted key {key} in bucket {index}")

    def search(self, key):
        index = self.hash_key(key)

        for existing_key, value in self.buckets[index]:
            if existing_key == key:
                print(f"Found key {key}: {value}")
                return value

        print(f"Key {key} not found")
        return None

    def display(self):
        for index, bucket in enumerate(self.buckets):
            print(f"Bucket {index}: {bucket}")


index = HashIndex(5)

index.insert(10, "Aman")
index.insert(15, "Riya")
index.insert(20, "Karan")

index.search(15)
index.search(25)

index.display()

