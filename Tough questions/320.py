
class ShadowPaging:
    def __init__(self):
        self.shadow_page_table = {
            "A": 100,
            "B": 200
        }

        self.current_page_table = self.shadow_page_table.copy()

    def update(self, item, value):
        self.current_page_table[item] = value
        print(f"Updated {item} = {value}")

    def commit(self):
        self.shadow_page_table = self.current_page_table.copy()
        print("Commit successful")

    def crash_recovery(self):
        self.current_page_table = self.shadow_page_table.copy()
        print("Recovered Database:", self.current_page_table)


db = ShadowPaging()

db.update("A", 150)
db.commit()

db.update("B", 300)

print("Crash Occurred!")
db.crash_recovery()
