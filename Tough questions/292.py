# Lock Compatibility Matrix


class LockCompatibility:
    def __init__(self):
        self.matrix = {
            "S": {"S": True, "X": False},
            "X": {"S": False, "X": False}
        }

    def check_compatibility(self, existing, requested):
        if self.matrix[existing][requested]:
            print(existing, "and", requested, ": Compatible")
        else:
            print(existing, "and", requested, ": Not Compatible")


db = LockCompatibility()

db.check_compatibility("S", "S")
db.check_compatibility("S", "X")
db.check_compatibility("X", "S")
db.check_compatibility("X", "X")
