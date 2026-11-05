# Shard Rebalancing Simulator


class ShardManager:
    def __init__(self, shard_count):
        self.shards = {
            i: [] for i in range(shard_count)
        }

    def add_record(self, record):
        shard_id = min(
            self.shards,
            key=lambda sid: len(self.shards[sid])
        )

        self.shards[shard_id].append(record)

    def show_shards(self):
        for shard_id, records in self.shards.items():
            print(f"Shard {shard_id}: {records}")

    def rebalance(self, new_count):
        records = []

        for shard in self.shards.values():
            records.extend(shard)

        self.shards = {
            i: [] for i in range(new_count)
        }

        for index, record in enumerate(records):
            shard_id = index % new_count
            self.shards[shard_id].append(record)

        print("Shards rebalanced successfully")


manager = ShardManager(2)

for record in ["A", "B", "C", "D", "E", "F"]:
    manager.add_record(record)

print("Before rebalancing:")
manager.show_shards()

manager.rebalance(3)

print("After rebalancing:")
manager.show_shards()
