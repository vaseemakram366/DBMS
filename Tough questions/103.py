# Database Transaction Log Shipping


import copy


class DatabaseNode:
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.log = []
        self.last_applied_lsn = 0

    def commit(self, operation, key, value):
        lsn = len(self.log) + 1

        entry = {
            "lsn": lsn,
            "operation": operation,
            "key": key,
            "value": value
        }

        self.apply(entry)
        self.log.append(entry)

        print(f"{self.name}: committed LSN {lsn}")
        return entry

    def apply(self, entry):
        operation = entry["operation"]
        key = entry["key"]

        if operation == "SET":
            self.data[key] = entry["value"]

        elif operation == "DELETE":
            self.data.pop(key, None)

        else:
            raise ValueError("Unsupported operation")

        self.last_applied_lsn = entry["lsn"]

    def ship_logs_to(self, replica):
        shipped = 0

        for entry in self.log:
            if entry["lsn"] > replica.last_applied_lsn:
                replica.apply(copy.deepcopy(entry))
                replica.log.append(copy.deepcopy(entry))
                shipped += 1

        print(
            f"Shipped {shipped} log entries "
            f"from {self.name} to {replica.name}"
        )

    def show(self):
        print(f"\n{self.name} database:", self.data)
        print("Last applied LSN:", self.last_applied_lsn)


primary = DatabaseNode("Primary")
replica = DatabaseNode("Replica")

primary.commit("SET", "user_1", "Aman")
primary.commit("SET", "user_2", "Riya")
primary.commit("SET", "user_1", "Rahul")

print("\nBefore log shipping:")
primary.show()
replica.show()

primary.ship_logs_to(replica)

print("\nAfter log shipping:")
primary.show()
replica.show()

primary.commit("DELETE", "user_2", None)
primary.ship_logs_to(replica)

print("\nAfter the next synchronization:")
primary.show()
replica.show()
