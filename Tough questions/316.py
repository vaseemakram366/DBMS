# feat: implement log-based database recovery


class UndoRedo:
    def __init__(self):
        self.database = {"A": 100}
        self.log = []

    def update(self, item, new_value):
        old_value = self.database[item]

        self.log.append({
            "item": item,
            "old": old_value,
            "new": new_value
        })

        self.database[item] = new_value

        print(f"Updated {item}: {new_value}")

    def undo(self):
        if not self.log:
            print("Nothing to undo")
            return

        entry = self.log[-1]
        self.database[entry["item"]] = entry["old"]

        print("UNDO:", self.database)

    def redo(self):
        if not self.log:
            print("Nothing to redo")
            return

        entry = self.log[-1]
        self.database[entry["item"]] = entry["new"]

        print("REDO:", self.database)


db = UndoRedo()

db.update("A", 200)
db.undo()
db.redo()
