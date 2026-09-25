# Database Sharding Router

import hashlib


class Shard:
    def __init__(self, shard_id):
        self.shard_id = shard_id
        self.data = {}

    def insert(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def delete(self, key):
        if key in self.data:
            del self.data[key]

    def show(self):
        print(f"Shard {self.shard_id}: {self.data}")


class ShardingRouter:
    def __init__(self, shard_count=4):
        self.shards = [
            Shard(i)
            for i in range(shard_count)
        ]

    def get_shard(self, key):
        digest = hashlib.sha256(
            str(key).encode()
        ).hexdigest()

        number = int(digest, 16)

        return self.shards[
            number % len(self.shards)
        ]

    def insert(self, key, value):
        shard = self.get_shard(key)

        shard.insert(key, value)

        print(
            f"INSERT {key} -> "
            f"Shard {shard.shard_id}"
        )

    def get(self, key):
        shard = self.get_shard(key)

        value = shard.get(key)

        print(
            f"GET {key} -> "
            f"Shard {shard.shard_id}"
        )

        return value

    def delete(self, key):
        shard = self.get_shard(key)

        shard.delete(key)

        print(
            f"DELETE {key} -> "
            f"Shard {shard.shard_id}"
        )

    def show_distribution(self):
        print("\nShard Distribution:")

        for shard in self.shards:
            shard.show()


router = ShardingRouter(4)

users = {
    101: "Amit",
    102: "Rahul",
    103: "Vaseem",
    104: "Neha",
    105: "Arjun",
    106: "Riya",
    107: "Karan",
    108: "Priya"
}

for user_id, name in users.items():
    router.insert(user_id, name)

print("\nRead Operations:")

print(router.get(103))
print(router.get(107))

router.delete(105)

router.show_distribution()