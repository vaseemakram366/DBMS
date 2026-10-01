# Change Data Capture (CDC) Engine

from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChangeEvent:
    sequence: int
    operation: str
    table: str
    key: int
    before: dict | None
    after: dict | None
    timestamp: str


class CDCEngine:
    def __init__(self):
        self.tables = {}
        self.change_log = []
        self.sequence = 0

    def create_table(self, name):
        self.tables[name] = {}

    def _record_change(
        self,
        operation,
        table,
        key,
        before,
        after
    ):
        self.sequence += 1

        event = ChangeEvent(
            sequence=self.sequence,
            operation=operation,
            table=table,
            key=key,
            before=before.copy() if before else None,
            after=after.copy() if after else None,
            timestamp=datetime.now().isoformat()
        )

        self.change_log.append(event)

    def insert(self, table, key, row):
        if key in self.tables[table]:
            raise ValueError("Duplicate key")

        self.tables[table][key] = row.copy()

        self._record_change(
            "INSERT",
            table,
            key,
            None,
            row
        )

    def update(self, table, key, updates):
        if key not in self.tables[table]:
            raise ValueError("Row not found")

        before = self.tables[table][key].copy()

        self.tables[table][key].update(updates)

        after = self.tables[table][key].copy()

        self._record_change(
            "UPDATE",
            table,
            key,
            before,
            after
        )

    def delete(self, table, key):
        if key not in self.tables[table]:
            raise ValueError("Row not found")

        before = self.tables[table].pop(key)

        self._record_change(
            "DELETE",
            table,
            key,
            before,
            None
        )

    def get_changes(self, start_sequence=1):
        return [
            event
            for event in self.change_log
            if event.sequence >= start_sequence
        ]

    def show_changes(self):
        print("\nCDC Change Stream")
        print("-" * 70)

        for event in self.change_log:
            print(
                f"[{event.sequence}] "
                f"{event.operation:<6} "
                f"{event.table}[{event.key}]"
            )

            if event.before is not None:
                print("  BEFORE:", event.before)

            if event.after is not None:
                print("  AFTER :", event.after)


class Consumer:
    def __init__(self):
        self.last_sequence = 0

    def consume(self, cdc):
        events = cdc.get_changes(
            self.last_sequence + 1
        )

        for event in events:
            print(
                f"Consumer processed event "
                f"#{event.sequence}: "
                f"{event.operation}"
            )

            self.last_sequence = event.sequence


if __name__ == "__main__":
    cdc = CDCEngine()

    cdc.create_table("employees")

    cdc.insert(
        "employees",
        1,
        {
            "name": "Aman",
            "salary": 50000
        }
    )

    cdc.insert(
        "employees",
        2,
        {
            "name": "Rahul",
            "salary": 60000
        }
    )

    cdc.update(
        "employees",
        1,
        {
            "salary": 70000
        }
    )

    cdc.delete(
        "employees",
        2
    )

    cdc.show_changes()

    print("\nStarting Consumer:")

    consumer = Consumer()
    consumer.consume(cdc)

    print("\nNew change:")

    cdc.insert(
        "employees",
        3,
        {
            "name": "Priya",
            "salary": 55000
        }
    )

    consumer.consume(cdc)