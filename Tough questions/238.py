# Transaction Rollback Simulator


class Transaction:
    def __init__(self, database):
        self.database = database
        self.undo_log = []
        self.active = True

    def write(self, key, value):
        if not self.active:
            print("Transaction is closed.")
            return

        old_value = self.database.get(key)
        self.undo_log.append((key, old_value))
        self.database[key] = value

        print(f"Write: {key} = {value}")

    def commit(self):
        if not self.active:
            print("Transaction is closed.")
            return

        self.undo_log.clear()
        self.active = False
        print("Transaction committed.")

    def rollback(self):
        if not self.active:
            print("Transaction is closed.")
            return

        for key, old_value in reversed(self.undo_log):
            if old_value is None:
                self.database.pop(key, None)
            else:
                self.database[key] = old_value

        self.undo_log.clear()
        self.active = False
        print("Transaction rolled back.")


database = {"balance": 1000}
print("Before:", database)

t1 = Transaction(database)
t1.write("balance", 800)
t1.write("balance", 500)
t1.rollback()

print("After:", database)
