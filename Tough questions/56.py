# Predicate Locking & Phantom Prevention

class PredicateLock:
    def __init__(self, transaction_id, column, operator, value):
        self.transaction_id = transaction_id
        self.column = column
        self.operator = operator
        self.value = value

    def matches(self, row):
        row_value = row[self.column]

        if self.operator == ">":
            return row_value > self.value

        if self.operator == ">=":
            return row_value >= self.value

        if self.operator == "<":
            return row_value < self.value

        if self.operator == "<=":
            return row_value <= self.value

        if self.operator == "==":
            return row_value == self.value

        return False


class PredicateLockManager:
    def __init__(self):
        self.locks = []

    def acquire(self, transaction_id, column, operator, value):
        lock = PredicateLock(
            transaction_id,
            column,
            operator,
            value
        )

        self.locks.append(lock)

        print(
            f"T{transaction_id} acquired predicate lock: "
            f"{column} {operator} {value}"
        )

    def check_insert(self, transaction_id, row):
        for lock in self.locks:
            if lock.transaction_id != transaction_id:
                if lock.matches(row):
                    return False

        return True

    def release(self, transaction_id):
        self.locks = [
            lock for lock in self.locks
            if lock.transaction_id != transaction_id
        ]


class Database:
    def __init__(self):
        self.rows = []
        self.lock_manager = PredicateLockManager()

    def select(self, transaction_id, column, operator, value):
        self.lock_manager.acquire(
            transaction_id,
            column,
            operator,
            value
        )

        result = []

        for row in self.rows:
            if PredicateLock(
                transaction_id,
                column,
                operator,
                value
            ).matches(row):
                result.append(row)

        return result

    def insert(self, transaction_id, row):
        if not self.lock_manager.check_insert(
            transaction_id,
            row
        ):
            print(
                f"INSERT blocked for T{transaction_id}: "
                f"predicate lock conflict"
            )
            return False

        self.rows.append(row)

        print(
            f"T{transaction_id} inserted: {row}"
        )

        return True

    def commit(self, transaction_id):
        self.lock_manager.release(transaction_id)
        print(f"T{transaction_id} committed")


if __name__ == "__main__":
    db = Database()

    db.rows = [
        {"id": 1, "salary": 40000},
        {"id": 2, "salary": 60000},
        {"id": 3, "salary": 80000}
    ]

    print("T1 executes range query:")

    result = db.select(
        1,
        "salary",
        ">",
        50000
    )

    print("Result:", result)

    print("\nT2 tries to insert matching row:")

    db.insert(
        2,
        {
            "id": 4,
            "salary": 70000
        }
    )

    print("\nT1 commits:")

    db.commit(1)

    print("\nT2 retries insert:")

    db.insert(
        2,
        {
            "id": 4,
            "salary": 70000
        }
    )