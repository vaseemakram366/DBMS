# Zone Map Index — Min/Max Data Skipping

class ZoneMap:
    def __init__(self):
        self.blocks = []

    def add_block(self, values):
        if not values:
            return

        block = {
            "min": min(values),
            "max": max(values),
            "values": values
        }

        self.blocks.append(block)

    def query_greater_equal(self, value):
        result = []

        for block in self.blocks:
            if block["max"] < value:
                continue

            for item in block["values"]:
                if item >= value:
                    result.append(item)

        return result

    def query_less_equal(self, value):
        result = []

        for block in self.blocks:
            if block["min"] > value:
                continue

            for item in block["values"]:
                if item <= value:
                    result.append(item)

        return result

    def query_range(self, low, high):
        result = []

        for block in self.blocks:
            if block["max"] < low or block["min"] > high:
                continue

            for item in block["values"]:
                if low <= item <= high:
                    result.append(item)

        return result

    def show_metadata(self):
        for i, block in enumerate(self.blocks):
            print(
                f"Block {i}: "
                f"min={block['min']}, "
                f"max={block['max']}"
            )


class ColumnStore:
    def __init__(self):
        self.price_index = ZoneMap()

    def insert_block(self, prices):
        self.price_index.add_block(prices)

    def query_price(self, low, high):
        return self.price_index.query_range(low, high)


db = ColumnStore()

db.insert_block([10, 20, 30, 40])
db.insert_block([100, 120, 150, 180])
db.insert_block([300, 350, 400, 450])
db.insert_block([500, 550, 600, 650])

db.price_index.show_metadata()

print("\nQuery: price between 500 and 600")
print(db.query_price(500, 600))