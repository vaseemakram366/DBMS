# Distributed Database Sharding


class DistributedDatabase:
    def __init__(self, shard_count):
        self.shards = {
            i: {} for i in range(shard_count)
        }

    def insert(self, student_id, name):
        shard_id = student_id % len(self.shards)

        self.shards[shard_id][student_id] = name

        print(
            f"Student {student_id} stored in Shard {shard_id}"
        )

    def show_shards(self):
        for shard_id, data in self.shards.items():
            print(f"Shard {shard_id}:", data)


db = DistributedDatabase(3)

db.insert(1, "Alice")
db.insert(2, "Bob")
db.insert(3, "Charlie")
db.insert(4, "David")
db.insert(5, "Emma")
db.insert(6, "Frank")

db.show_shards()
