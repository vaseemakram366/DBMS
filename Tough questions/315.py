# Database Recovery Using Log-Based Recovery


class LogBasedRecovery:
    def __init__(self):
        self.database = {"A": 100}
        self.log = []

    def execute_transaction(self, transaction, item, new_value):
        old_value = self.database[item]

        self.log.append(
            (transaction, "START", None, None)
        )

        self.log.append(
            (transaction, "UPDATE", item, old_value, new_value)
        )

        self.database[item] = new_value

        self.log.append(
            (transaction, "COMMIT", None, None)
        )

        print(f"{transaction} updated {item}: {old_value} -> {new_value}")

    def show_log(self):
        print("\nTransaction Log:")

        for entry in self.log:
            print(entry)

        print("\nDatabase:", self.database)


db = LogBasedRecovery()

db.execute_transaction("T1", "A", 200)
db.show_log()
