# T-Digest Approximate Percentile Estimator


import bisect
import random


class SimpleDigest:
    def __init__(self, max_centroids=100):
        if max_centroids < 2:
            raise ValueError("Use at least 2 centroids")

        self.max_centroids = max_centroids
        self.centroids = []
        self.count = 0

    def add(self, value):
        value = float(value)

        if not self.centroids:
            self.centroids.append([value, 1])
            self.count += 1
            return

        means = [c[0] for c in self.centroids]
        index = bisect.bisect_left(means, value)

        candidates = []

        if index > 0:
            candidates.append(index - 1)

        if index < len(self.centroids):
            candidates.append(index)

        nearest = min(
            candidates,
            key=lambda i: abs(self.centroids[i][0] - value)
        )

        if len(self.centroids) >= self.max_centroids:
            mean, weight = self.centroids[nearest]

            new_mean = (
                mean * weight + value
            ) / (weight + 1)

            self.centroids[nearest] = [
                new_mean,
                weight + 1
            ]
        else:
            self.centroids.insert(index, [value, 1])

        self.count += 1
        self.centroids.sort(key=lambda c: c[0])

    def percentile(self, q):
        if not 0 <= q <= 100:
            raise ValueError("Percentile must be between 0 and 100")

        if self.count == 0:
            return None

        target = q / 100 * (self.count - 1)
        cumulative = 0

        for mean, weight in self.centroids:
            if target < cumulative + weight:
                return mean

            cumulative += weight

        return self.centroids[-1][0]

    def merge(self, other):
        for mean, weight in other.centroids:
            for _ in range(weight):
                self.add(mean)


random.seed(42)

digest = SimpleDigest(max_centroids=50)
response_times = [
    random.expovariate(1 / 100)
    for _ in range(1000)
]

for time_ms in response_times:
    digest.add(time_ms)

print("Total observations:", digest.count)
print("Estimated median:", round(digest.percentile(50), 2), "ms")
print("Estimated P95:", round(digest.percentile(95), 2), "ms")
print("Estimated P99:", round(digest.percentile(99), 2), "ms")
print("Centroids stored:", len(digest.centroids))
