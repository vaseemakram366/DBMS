# Database Savepoint and Partial Rollback Simulator


class SavepointSimulator:
    def __init__(self):
        self.database = {"balance": 1000}
        self.active = False
        self.undo_log = []
        self.savepoints = {}

    def begin(self):
        if self.active:
            raise ValueError("Transaction already active")

        self.active = True
        self.undo_log = []
        self.savepoints = {}
        print("Transaction started")

    def update(self, item, value):
        if not self.active:
            raise ValueError("No active transaction")

        old_value = self.database[item]

        self.undo_log.append((item, old_value))
        self.database[item] = value

        print(f"UPDATE {item}: {old_value} -> {value}")

    def savepoint(self, name):
        if not self.active:
            raise ValueError("No active transaction")

        self.savepoints[name] = len(self.undo_log)
        print(f"SAVEPOINT {name} created")

    def rollback_to(self, name):
        if not self.active:
            raise ValueError("No active transaction")

        if name not in self.savepoints:
            raise ValueError("Savepoint does not exist")

        position = self.savepoints[name]

        while len(self.undo_log) > position:
            item, old_value = self.undo_log.pop()
            current_value = self.database[item]
            self.database[item] = old_value

            print(
                f"UNDO {item}: {current_value} -> {old_value}"
            )

        # Savepoints created after the target are discarded.
        self.savepoints = {
            key: value
            for key, value in self.savepoints.items()
            if value <= position
        }

        print(f"Rolled back to {name}")

    def commit(self):
        if not self.active:
            raise ValueError("No active transaction")

        self.active = False
        self.undo_log.clear()
        self.savepoints.clear()
        print("Transaction committed")

    def show_database(self):
        print("Database:", self.database)


db = SavepointSimulator()

db.show_database()
db.begin()

db.update("balance", 900)
db.savepoint("SP1")

db.update("balance", 700)
db.update("balance", 500)

db.rollback_to("SP1")
db.show_database()

db.commit()
