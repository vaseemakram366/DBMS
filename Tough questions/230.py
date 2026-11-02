# Lock Compatibility Matrix


class LockCompatibility:
    matrix = {
        "S": {"S": True, "X": False},
        "X": {"S": False, "X": False}
    }

    @classmethod
    def is_compatible(cls, existing, requested):
        return cls.matrix[existing][requested]


tests = [
    ("S", "S"),
    ("S", "X"),
    ("X", "S"),
    ("X", "X")
]

print("Existing | Requested | Result")
print("-" * 32)

for existing, requested in tests:
    result = LockCompatibility.is_compatible(
        existing, requested
    )
    status = "ALLOW" if result else "DENY"

    print(f"{existing:^8} | {requested:^9} | {status}")
