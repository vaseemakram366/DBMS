# Learned Index — ML-Based Database Index

class LearnedIndex:
    def __init__(self, data):
        self.data = sorted(data)
        self.n = len(self.data)

        self.min_key = self.data[0]
        self.max_key = self.data[-1]

    def predict_position(self, key):
        if key <= self.min_key:
            return 0

        if key >= self.max_key:
            return self.n - 1

        ratio = (
            (key - self.min_key) /
            (self.max_key - self.min_key)
        )

        return int(ratio * (self.n - 1))

    def search(self, key, error_bound=5):
        predicted = self.predict_position(key)

        left = max(0, predicted - error_bound)
        right = min(
            self.n,
            predicted + error_bound + 1
        )

        for i in range(left, right):
            if self.data[i] == key:
                return i

        return -1


data = [
    10, 20, 30, 40, 50,
    60, 70, 80, 90, 100,
    110, 120, 130, 140, 150
]

index = LearnedIndex(data)

for key in [10, 70, 120, 150, 999]:
    position = index.search(key)

    if position != -1:
        print(
            f"Key {key} found at position {position}"
        )
    else:
        print(f"Key {key} not found")