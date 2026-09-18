# Database Index — Hash Index with Collision Handling

class HashIndex:

    def __init__(self, size=7):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return key % self.size

    def insert(self, key, record):
        index = self._hash(key)

        for existing_key, _ in self.table[index]:
            if existing_key == key:
                print("Key already exists:", key)
                return

        self.table[index].append(
            (key, record)
        )

        print(
            "Inserted:",
            key,
            "->",
            record,
            "Bucket:",
            index
        )

    def search(self, key):
        index = self._hash(key)

        for existing_key, record in self.table[index]:
            if existing_key == key:
                return record

        return None

    def delete(self, key):
        index = self._hash(key)

        for i, (existing_key, record) in enumerate(
            self.table[index]
        ):
            if existing_key == key:
                self.table[index].pop(i)
                print("Deleted:", key)
                return True

        print("Key not found:", key)
        return False

    def display(self):
        print("\nHash Index:")

        for i, bucket in enumerate(self.table):
            print(
                f"Bucket {i}:",
                bucket
            )


index = HashIndex(5)

index.insert(10, "Vaseem")
index.insert(15, "Rahul")
index.insert(20, "Aman")
index.insert(7, "Sara")
index.insert(12, "Karan")
index.insert(17, "Neha")

index.display()

print("\nSearch 15:")
print(index.search(15))

print("\nSearch 100:")
print(index.search(100))

index.delete(15)

index.display()