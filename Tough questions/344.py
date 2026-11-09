# Database Lock Compatibility Matrix


class LockCompatibility:
    def __init__(self):
        self.matrix = {
            "S": {"S": True, "X": False},
            "X": {"S": False, "X": False}
        }

    def check(self, lock1, lock2):
        if lock1 not in self.matrix or lock2 not in self.matrix:
            print("Invalid Lock Type")
            return

        compatible = self.matrix[lock1][lock2]

        if compatible:
            print(f"{lock1} + {lock2}: Compatible")
        else:
            print(f"{lock1} + {lock2}: Not Compatible")


obj = LockCompatibility()

obj.check("S", "S")
obj.check("S", "X")
obj.check("X", "S")
obj.check("X", "X")
