# Mini SQL Engine

class MiniDB:

    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns):

        if name in self.tables:
            print("Table already exists")
            return

        self.tables[name] = {
            "columns": columns,
            "rows": []
        }

        print("Table created:", name)

    def insert(self, table, values):

        if table not in self.tables:
            print("Table does not exist")
            return

        columns = self.tables[table]["columns"]

        if len(columns) != len(values):
            print("Column count mismatch")
            return

        row = dict(zip(columns, values))

        self.tables[table]["rows"].append(row)

        print("Row inserted")

    def select(self, table, columns=None):

        if table not in self.tables:
            print("Table does not exist")
            return

        rows = self.tables[table]["rows"]

        if columns is None:
            columns = self.tables[table]["columns"]

        print("\n", columns)

        for row in rows:
            print(
                [row[column] for column in columns]
            )


db = MiniDB()

db.create_table(
    "students",
    ["id", "name", "marks"]
)

db.insert(
    "students",
    [1, "Vaseem", 92]
)

db.insert(
    "students",
    [2, "Rahul", 85]
)

db.insert(
    "students",
    [3, "Aman", 95]
)

db.select("students")

print("\nOnly name and marks:")

db.select(
    "students",
    ["name", "marks"]
)