# Database Lock Escalation Simulator


class LockEscalationSimulator:

    def __init__(self, threshold=5):
        self.threshold = threshold
        self.row_locks = {}
        self.table_locks = {}

    def acquire_row_lock(self, tx_id, table, row_id):
        table_owner = self.table_locks.get(table)

        if table_owner is not None and table_owner != tx_id:
            print(f"DENIED: {tx_id} cannot lock {table}[{row_id}]")
            return False

        key = (table, row_id)
        owner = self.row_locks.get(key)

        if owner is not None and owner != tx_id:
            print(f"DENIED: {tx_id} cannot lock {table}[{row_id}]")
            return False

        if owner == tx_id:
            return True

        self.row_locks[key] = tx_id
        print(f"ROW LOCK: {tx_id} -> {table}[{row_id}]")

        self._check_escalation(tx_id, table)
        return True

    def _check_escalation(self, tx_id, table):
        held_rows = [
            key for key, owner in self.row_locks.items()
            if owner == tx_id and key[0] == table
        ]

        if len(held_rows) < self.threshold:
            return

        other_owners = [
            owner
            for (locked_table, _), owner in self.row_locks.items()
            if locked_table == table and owner != tx_id
        ]

        if other_owners:
            print(f"ESCALATION DEFERRED: {table} has other row-lock owners")
            return

        for key in held_rows:
            del self.row_locks[key]

        self.table_locks[table] = tx_id
        print(
            f"LOCK ESCALATION: {tx_id} now holds "
            f"a table lock on {table}"
        )

    def release_all(self, tx_id):
        self.row_locks = {
            key: owner
            for key, owner in self.row_locks.items()
            if owner != tx_id
        }

        self.table_locks = {
            table: owner
            for table, owner in self.table_locks.items()
            if owner != tx_id
        }

        print(f"Released all locks held by {tx_id}.")

    def show_status(self):
        print("\nROW LOCKS:", self.row_locks)
        print("TABLE LOCKS:", self.table_locks)


simulator = LockEscalationSimulator(threshold=3)

simulator.acquire_row_lock("T1", "Employees", 101)
simulator.acquire_row_lock("T1", "Employees", 102)
simulator.acquire_row_lock("T1", "Employees", 103)

simulator.show_status()

simulator.acquire_row_lock("T2", "Employees", 104)

simulator.release_all("T1")
simulator.acquire_row_lock("T2", "Employees", 104)

simulator.show_status()
