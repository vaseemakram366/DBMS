# MVCC Version Garbage Collector

from dataclasses import dataclass


@dataclass
class Version:
    value: object
    created_at: int
    deleted_at: int | None = None


class MVCCStorage:
    def __init__(self):
        self.data = {}
        self.active_transactions = set()
        self.clock = 0

    def begin(self):
        self.clock += 1
        transaction_id = self.clock
        self.active_transactions.add(transaction_id)

        print(f"Transaction {transaction_id} started")
        return transaction_id

    def commit(self, transaction_id):
        self.active_transactions.discard(transaction_id)
        print(f"Transaction {transaction_id} committed")

    def write(self, key, value, transaction_id):
        versions = self.data.setdefault(key, [])

        if versions:
            versions[-1].deleted_at = transaction_id

        versions.append(
            Version(
                value=value,
                created_at=transaction_id
            )
        )

    def read(self, key, transaction_id):
        versions = self.data.get(key, [])

        visible = None

        for version in versions:
            if version.created_at <= transaction_id:
                if (
                    version.deleted_at is None
                    or version.deleted_at > transaction_id
                ):
                    visible = version

        return visible.value if visible else None

    def garbage_collect(self):
        if self.active_transactions:
            oldest_active = min(self.active_transactions)
        else:
            oldest_active = self.clock + 1

        for key in list(self.data.keys()):
            versions = self.data[key]

            if len(versions) <= 1:
                continue

            kept = []

            for version in versions:
                if (
                    version.deleted_at is None
                    or version.deleted_at >= oldest_active
                ):
                    kept.append(version)

            if not kept:
                kept.append(versions[-1])

            self.data[key] = kept

    def show_versions(self):
        print("\nMVCC Versions")
        print("-" * 50)

        for key, versions in self.data.items():
            print(f"\nKey: {key}")

            for version in versions:
                print(
                    f"Value={version.value}, "
                    f"Created={version.created_at}, "
                    f"Deleted={version.deleted_at}"
                )


if __name__ == "__main__":
    db = MVCCStorage()

    t1 = db.begin()
    db.write("A", 100, t1)
    db.commit(t1)

    t2 = db.begin()

    t3 = db.begin()
    db.write("A", 200, t3)
    db.commit(t3)

    t4 = db.begin()
    db.write("A", 300, t4)
    db.commit(t4)

    print("\nOld transaction sees:")
    print("T2 ->", db.read("A", t2))

    db.show_versions()

    db.commit(t2)

    print("\nRunning garbage collection...")
    db.garbage_collect()

    db.show_versions()