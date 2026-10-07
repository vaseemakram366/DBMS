# Approximate Distinct Count

import hashlib
import math


class HyperLogLog:
    def __init__(self, precision=5):
        self.precision = precision
        self.bucket_count = 1 << precision
        self.registers = [0] * self.bucket_count

    def _hash(self, value):
        data = str(value).encode()
        digest = hashlib.sha256(data).digest()
        return int.from_bytes(digest, "big")

    def _rho(self, value, bits):
        if value == 0:
            return bits + 1

        return bits - value.bit_length() + 1

    def add(self, value):
        hashed = self._hash(value)

        bucket = hashed >> (256 - self.precision)

        remaining_bits = 256 - self.precision
        remaining = hashed & ((1 << remaining_bits) - 1)

        rank = self._rho(remaining, remaining_bits)

        self.registers[bucket] = max(
            self.registers[bucket],
            rank
        )

    def count(self):
        m = self.bucket_count

        alpha = 0.7213 / (1 + 1.079 / m)

        harmonic_sum = sum(
            2 ** (-register)
            for register in self.registers
        )

        estimate = alpha * (m ** 2) / harmonic_sum

        return round(estimate)


class Database:
    def __init__(self):
        self.hll_indexes = {}

    def create_distinct_index(self, column):
        self.hll_indexes[column] = HyperLogLog()

    def insert(self, row):
        for column, hll in self.hll_indexes.items():
            if column in row:
                hll.add(row[column])

    def count_distinct(self, column):
        return self.hll_indexes[column].count()


db = Database()

db.create_distinct_index("user_id")

users = [
    101, 102, 103, 104, 105,
    101, 102, 106, 107, 108,
    103, 104, 109, 110, 111
]

for user_id in users:
    db.insert({"user_id": user_id})

print("Estimated distinct users:",
      db.count_distinct("user_id"))