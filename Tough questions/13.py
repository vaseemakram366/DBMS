# WHERE + UPDATE + DELETE


class MiniDB:

    def __init__(self):
        self.tables = {}

    # CREATE TABLE
    def create_table(self, name, columns):

        if name in self.tables:
            print("Table already exists")
            return

        self.tables[name] = {
            "columns": columns,
            "rows": []
        }

        print("Table created:", name)

    # INSERT
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

    # SELECT with WHERE
    def select(self, table, columns=None, where=None):

        if table not in self.tables:
            print("Table does not exist")
            return

        rows = self.tables[table]["rows"]

        if columns is None:
            columns = self.tables[table]["columns"]

        print("\n", columns)

        for row in rows:

            # WHERE condition
            if where is not None:

                column, operator, value = where

                if operator == "=" and row[column] != value:
                    continue

                if operator == ">" and row[column] <= value:
                    continue

                if operator == "<" and row[column] >= value:
                    continue

                if operator == ">=" and row[column] < value:
                    continue

                if operator == "<=" and row[column] > value:
                    continue

            print([row[column] for column in columns])

    # UPDATE
    def update(self, table, set_column, set_value, where=None):

        if table not in self.tables:
            print("Table does not exist")
            return

        rows = self.tables[table]["rows"]

        count = 0

        for row in rows:

            if where is not None:

                column, operator, value = where

                if operator == "=" and row[column] != value:
                    continue

                if operator == ">" and row[column] <= value:
                    continue

                if operator == "<" and row[column] >= value:
                    continue

            row[set_column] = set_value
            count += 1

        print(count, "row(s) updated")

    # DELETE
    def delete(self, table, where=None):

        if table not in self.tables:
            print("Table does not exist")
            return

        rows = self.tables[table]["rows"]

        if where is None:
            self.tables[table]["rows"] = []
            print("All rows deleted")
            return

        column, operator, value = where

        new_rows = []
        count = 0

        for row in rows:

            match = False

            if operator == "=":
                match = row[column] == value

            elif operator == ">":
                match = row[column] > value

            elif operator == "<":
                match = row[column] < value

            if match:
                count += 1
            else:
                new_rows.append(row)

        self.tables[table]["rows"] = new_rows

        print(count, "row(s) deleted")


# -----------------------------
# TESTING
# -----------------------------

db = MiniDB()

db.create_table(
    "students",
    ["id", "name", "marks"]
)

db.insert("students", [1, "Vaseem", 92])
db.insert("students", [2, "Rahul", 85])
db.insert("students", [3, "Aman", 95])


# SELECT *
print("\nAll students:")
db.select("students")


# SELECT WHERE marks > 90
print("\nMarks greater than 90:")
db.select(
    "students",
    ["name", "marks"],
    ("marks", ">", 90)
)


# UPDATE
print("\nUpdating Rahul's marks:")
db.update(
    "students",
    "marks",
    90,
    ("name", "=", "Rahul")
)

db.select("students")


# DELETE
print("\nDeleting students with marks < 90:")
db.delete(
    "students",
    ("marks", "<", 90)
)

db.select("students")