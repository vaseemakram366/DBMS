# Lock Compatibility Matrix


class LockCompatibility:
    def __init__(self):
        self.matrix = {
            "IS": {"IS": True, "IX": True, "S": True, "SIX": True, "X": False},
            "IX": {"IS": True, "IX": True, "S": False, "SIX": False, "X": False},
            "S":  {"IS": True, "IX": False, "S": True, "SIX": False, "X": False},
            "SIX":{"IS": True, "IX": False, "S": False, "SIX": False, "X": False},
            "X":  {"IS": False, "IX": False, "S": False, "SIX": False, "X": False}
        }

    def check(self, existing, requested):
        if self.matrix[existing][requested]:
            print(f"{existing} + {requested}: COMPATIBLE")
        else:
            print(f"{existing} + {requested}: NOT COMPATIBLE")


db = LockCompatibility()

db.check("S", "S")
db.check("S", "X")
db.check("IX", "IS")
db.check("X", "IS")
