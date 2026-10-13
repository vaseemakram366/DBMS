# Database Constraint Validation Engine


class ConstraintDatabase:
    def __init__(self):
        self.tables = {}
        self.schemas = {}

    def create_table(self, table_name, columns, primary_key,
                     not_null=None, unique=None, checks=None,
                     foreign_keys=None):
        if table_name in self.tables:
            raise ValueError("Table already exists")

        self.tables[table_name] = []
        self.schemas[table_name] = {
            "columns": set(columns),
            "primary_key": primary_key,
            "not_null": set(not_null or []),
            "unique": list(unique or []),
            "checks": list(checks or []),
            "foreign_keys": list(foreign_keys or [])
        }

    def validate(self, table_name, record, ignore=None):
        schema = self.schemas[table_name]
        rows = self.tables[table_name]

        unknown = set(record) - schema["columns"]
        if unknown:
            raise ValueError(f"Unknown columns: {unknown}")

        for column in schema["columns"]:
            record.setdefault(column, None)

        required = schema["not_null"] | {schema["primary_key"]}

        for column in required:
            if record.get(column) is None:
                raise ValueError(f"{column} cannot be NULL")

        constraints = [
            [schema["primary_key"]],
            *schema["unique"]
        ]

        for columns in constraints:
            values = tuple(record.get(c) for c in columns)

            if any(value is None for value in values):
                continue

            for row in rows:
                if row is ignore:
                    continue

                existing = tuple(row.get(c) for c in columns)

                if existing == values:
                    raise ValueError(
                        f"UNIQUE constraint failed: {columns}"
                    )

        for description, condition in schema["checks"]:
            if not condition(record):
                raise ValueError(
                    f"CHECK constraint failed: {description}"
                )

        for column, parent_table, parent_column in schema["foreign_keys"]:
            value = record.get(column)

            if value is None:
                continue

            if parent_table not in self.tables:
                raise ValueError("Referenced table does not exist")

            found = any(
                row.get(parent_column) == value
                for row in self.tables[parent_table]
            )

            if not found:
                raise ValueError(
                    f"FOREIGN KEY constraint failed: {column}"
                )

    def insert(self, table_name, record):
        candidate = record.copy()
        self.validate(table_name, candidate)
        self.tables[table_name].append(candidate)
        print("Inserted:", candidate)

    def update(self, table_name, primary_key_value, changes):
        schema = self.schemas[table_name]
        pk = schema["primary_key"]

        for row in self.tables[table_name]:
            if row[pk] == primary_key_value:
                candidate = row.copy()
                candidate.update(changes)

                self.validate(table_name, candidate, ignore=row)
                row.update(candidate)

                print("Updated:", row)
                return

        raise ValueError("Record not found")

    def select(self, table_name):
        return [row.copy() for row in self.tables[table_name]]


db = ConstraintDatabase()

db.create_table(
    "departments",
    columns=["dept_id", "name"],
    primary_key="dept_id",
    not_null=["name"],
    unique=[["name"]]
)

db.create_table(
    "students",
    columns=["roll_no", "name", "age", "dept_id"],
    primary_key="roll_no",
    not_null=["name", "age"],
    unique=[["name", "dept_id"]],
    checks=[
        ("age must be positive", lambda r: r["age"] > 0)
    ],
    foreign_keys=[
        ("dept_id", "departments", "dept_id")
    ]
)

db.insert("departments", {
    "dept_id": 1,
    "name": "CSE"
})

db.insert("students", {
    "roll_no": 101,
    "name": "Aman",
    "age": 20,
    "dept_id": 1
})

db.update("students", 101, {"age": 21})

print("\nStudents:", db.select("students"))

# Try invalid data:
try:
    db.insert("students", {
        "roll_no": 102,
        "name": "Riya",
        "age": -5,
        "dept_id": 1
    })
except ValueError as error:
    print("Rejected:", error)
