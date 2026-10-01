# Lock Escalation Manager

from collections import defaultdict


class LockEscalationManager:
    def __init__(self, escalation_threshold=3):
        self.escalation_threshold = escalation_threshold
        self.row_locks = defaultdict(set)
        self.table_locks = {}

    def acquire_row_lock(self, transaction_id, table, row_id):
        if table in self.table_locks:
            owner = self.table_locks[table]

            if owner != transaction_id:
                print(
                    f"T{transaction_id} blocked: "
                    f"{table} locked by T{owner}"
                )
                return False

        self.row_locks[transaction_id].add(
            (table, row_id)
        )

        print(
            f"T{transaction_id} acquired row lock "
            f"{table}[{row_id}]"
        )

        self.check_escalation(transaction_id, table)

        return True

    def check_escalation(self, transaction_id, table):
        locked_rows = [
            row
            for locked_table, row in self.row_locks[transaction_id]
            if locked_table == table
        ]

        if len(locked_rows) >= self.escalation_threshold:
            self.escalate(
                transaction_id,
                table,
                locked_rows
            )

    def escalate(self, transaction_id, table, rows):
        if table in self.table_locks:
            return

        self.table_locks[table] = transaction_id

        self.row_locks[transaction_id] = {
            lock
            for lock in self.row_locks[transaction_id]
            if lock[0] != table
        }

        print(
            f"\nLOCK ESCALATION:"
            f"\nT{transaction_id} converted "
            f"{len(rows)} row locks into "
            f"table lock on {table}\n"
        )

    def release_all(self, transaction_id):
        self.row_locks.pop(transaction_id, None)

        tables_to_release = [
            table
            for table, owner in self.table_locks.items()
            if owner == transaction_id
        ]

        for table in tables_to_release:
            del self.table_locks[table]

        print(
            f"T{transaction_id} released all locks"
        )

    def show_locks(self):
        print("\nCurrent Locks")
        print("-" * 40)

        for transaction, locks in self.row_locks.items():
            print(
                f"T{transaction} Row Locks: {locks}"
            )

        for table, transaction in self.table_locks.items():
            print(
                f"{table} → Table Lock by T{transaction}"
            )


if __name__ == "__main__":
    manager = LockEscalationManager(
        escalation_threshold=3
    )

    manager.acquire_row_lock(1, "employees", 101)
    manager.acquire_row_lock(1, "employees", 102)
    manager.acquire_row_lock(1, "employees", 103)

    manager.show_locks()

    print("\nT2 tries to access employees:")

    manager.acquire_row_lock(
        2,
        "employees",
        104
    )

    print("\nT1 commits:")

    manager.release_all(1)

    print("\nT2 retries:")

    manager.acquire_row_lock(
        2,
        "employees",
        104
    )

    manager.show_locks()