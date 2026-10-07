# Referential Integrity Constraint Manager

class Table:
    def __init__(self, name, primary_key):
        self.name = name
        self.primary_key = primary_key
        self.rows = {}

    def insert(self, row):
        key = row[self.primary_key]

        if key in self.rows:
            raise ValueError(f"Duplicate primary key: {key}")

        self.rows[key] = row

    def delete(self, key):
        if key in self.rows:
            del self.rows[key]


class ForeignKey:
    def __init__(self, child_table, child_column,
                 parent_table, parent_column,
                 on_delete="RESTRICT"):

        self.child_table = child_table
        self.child_column = child_column
        self.parent_table = parent_table
        self.parent_column = parent_column
        self.on_delete = on_delete


class Database:
    def __init__(self):
        self.tables = {}
        self.foreign_keys = []

    def create_table(self, name, primary_key):
        self.tables[name] = Table(name, primary_key)

    def add_foreign_key(self, child_table, child_column,
                        parent_table, parent_column,
                        on_delete="RESTRICT"):

        fk = ForeignKey(
            child_table,
            child_column,
            parent_table,
            parent_column,
            on_delete
        )

        self.foreign_keys.append(fk)

    def insert(self, table_name, row):
        table = self.tables[table_name]

        for fk in self.foreign_keys:
            if fk.child_table != table_name:
                continue

            value = row.get(fk.child_column)

            if value is None:
                continue

            parent = self.tables[fk.parent_table]

            if value not in parent.rows:
                raise ValueError(
                    f"Foreign key violation: "
                    f"{value} does not exist in {fk.parent_table}"
                )

        table.insert(row)

    def delete(self, table_name, key):
        table = self.tables[table_name]

        if key not in table.rows:
            return

        for fk in self.foreign_keys:
            if fk.parent_table != table_name:
                continue

            child = self.tables[fk.child_table]

            affected = []

            for child_key, row in child.rows.items():
                if row.get(fk.child_column) == key:
                    affected.append(child_key)

            if not affected:
                continue

            if fk.on_delete == "RESTRICT":
                raise ValueError(
                    f"Cannot delete {key}: "
                    f"referenced by {fk.child_table}"
                )

            elif fk.on_delete == "CASCADE":
                for child_key in affected:
                    self.delete(fk.child_table, child_key)

            elif fk.on_delete == "SET NULL":
                for child_key in affected:
                    child.rows[child_key][fk.child_column] = None

        table.delete(key)

    def show(self, table_name):
        table = self.tables[table_name]

        for row in table.rows.values():
            print(row)


db = Database()

db.create_table("departments", "id")
db.create_table("employees", "id")

db.add_foreign_key(
    "employees",
    "department_id",
    "departments",
    "id",
    on_delete="CASCADE"
)

db.insert("departments", {
    "id": 1,
    "name": "CSE"
})

db.insert("departments", {
    "id": 2,
    "name": "ECE"
})

db.insert("employees", {
    "id": 101,
    "name": "Rahul",
    "department_id": 1
})

db.insert("employees", {
    "id": 102,
    "name": "Aman",
    "department_id": 1
})

db.insert("employees", {
    "id": 103,
    "name": "Vikas",
    "department_id": 2
})

print("Before deleting department:")
db.show("employees")

db.delete("departments", 1)

print("\nAfter deleting department 1:")
db.show("employees")