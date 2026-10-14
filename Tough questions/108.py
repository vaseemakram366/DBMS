# Database Dead Tuple Vacuuming Engine


class MVCCDatabase:
    def __init__(self):
        self.rows = {}
        self.next_row_id = 1
        self.oldest_active_txn = float("inf")

    def insert(self, txn_id, data):
        row_id = self.next_row_id
        self.next_row_id += 1

        self.rows[row_id] = [{
            "data": data.copy(),
            "created_by": txn_id,
            "deleted_by": None
        }]

        return row_id

    def update(self, txn_id, row_id, new_data):
        versions = self.rows.get(row_id)

        if not versions:
            raise ValueError("Row not found")

        current = versions[-1]

        if current["deleted_by"] is not None:
            raise ValueError("Row is already deleted")

        current["deleted_by"] = txn_id

        versions.append({
            "data": new_data.copy(),
            "created_by": txn_id,
            "deleted_by": None
        })

    def delete(self, txn_id, row_id):
        versions = self.rows.get(row_id)

        if not versions:
            raise ValueError("Row not found")

        current = versions[-1]

        if current["deleted_by"] is not None:
            raise ValueError("Row is already deleted")

        current["deleted_by"] = txn_id

    def set_oldest_active_txn(self, txn_id):
        self.oldest_active_txn = txn_id

    def vacuum(self):
        removed = 0

        for row_id in list(self.rows):
            versions = self.rows[row_id]
            kept = []

            for version in versions:
                delete_txn = version["deleted_by"]

                if (
                    delete_txn is not None
                    and delete_txn < self.oldest_active_txn
                ):
                    removed += 1
                else:
                    kept.append(version)

            if kept:
                self.rows[row_id] = kept
            else:
                del self.rows[row_id]

        print(f"Vacuum removed {removed} obsolete versions")
        return removed

    def show(self):
        print("\nDatabase state:")

        for row_id, versions in self.rows.items():
            print(f"Row {row_id}: {versions}")


db = MVCCDatabase()

row1 = db.insert(1, {"name": "Aman", "salary": 30000})
db.update(2, row1, {"name": "Aman", "salary": 45000})

row2 = db.insert(3, {"name": "Riya", "salary": 40000})
db.delete(4, row2)

db.set_oldest_active_txn(5)

print("Before vacuum:")
db.show()

db.vacuum()

print("\nAfter vacuum:")
db.show()
