# Bitmap Index

class BitmapIndex:
    def __init__(self):
        self.index = {}
        self.rows = 0

    def build(self, values):
        self.rows = len(values)

        unique_values = set(values)

        for value in unique_values:
            bitmap = 0

            for i, current in enumerate(values):
                if current == value:
                    bitmap |= (1 << i)

            self.index[value] = bitmap

    def get_bitmap(self, value):
        return self.index.get(value, 0)

    def AND(self, value1, value2):
        return self.get_bitmap(value1) & self.get_bitmap(value2)

    def OR(self, value1, value2):
        return self.get_bitmap(value1) | self.get_bitmap(value2)

    def NOT(self, value):
        mask = (1 << self.rows) - 1
        return (~self.get_bitmap(value)) & mask

    def decode(self, bitmap):
        result = []

        for i in range(self.rows):
            if bitmap & (1 << i):
                result.append(i)

        return result

    def search(self, value):
        bitmap = self.get_bitmap(value)
        return self.decode(bitmap)

    def show(self):
        for value, bitmap in self.index.items():
            print(
                f"{value}: "
                f"{format(bitmap, f'0{self.rows}b')}"
            )


departments = [
    "CSE",
    "ECE",
    "CSE",
    "ME",
    "CSE",
    "ECE",
    "ME",
    "CSE"
]

index = BitmapIndex()
index.build(departments)

print("Bitmap Index:")
index.show()

print("\nCSE rows:")
print(index.search("CSE"))

print("\nCSE OR ECE:")
bitmap = index.OR("CSE", "ECE")
print(index.decode(bitmap))

print("\nCSE AND ECE:")
bitmap = index.AND("CSE", "ECE")
print(index.decode(bitmap))

print("\nNOT CSE:")
bitmap = index.NOT("CSE")
print(index.decode(bitmap))