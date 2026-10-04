# Database System Catalog

class SystemCatalog:
    def __init__(self):
        self.tables = {}
        self.indexes = {}

    def create_table(self, table_name, columns):
        if table_name in self.tables:
            raise ValueError("Table already exists")

        self.tables[table_name] = {
            "columns": columns,
            "row_count": 0
        }

    def drop_table(self, table_name):
        if table_name not in self.tables:
            return False

        del self.tables[table_name]

        indexes_to_delete = [
            name
            for name, index in self.indexes.items()
            if index["table"] == table_name
        ]

        for index_name in indexes_to_delete:
            del self.indexes[index_name]

        return True

    def add_rows(self, table_name, count=1):
        if table_name not in self.tables:
            raise ValueError("Table does not exist")

        self.tables[table_name]["row_count"] += count

    def create_index(self, index_name, table_name, column):
        if table_name not in self.tables:
            raise ValueError("Table does not exist")

        columns = self.tables[table_name]["columns"]

        if column not in columns:
            raise ValueError("Column does not exist")

        if index_name in self.indexes:
            raise ValueError("Index already exists")

        self.indexes[index_name] = {
            "table": table_name,
            "column": column
        }

    def get_table_schema(self, table_name):
        if table_name not in self.tables:
            return None

        return self.tables[table_name]["columns"]

    def list_tables(self):
        return list(self.tables.keys())

    def describe_table(self, table_name):
        if table_name not in self.tables:
            return None

        table = self.tables[table_name]

        print(f"\nTable: {table_name}")
        print("Columns:")

        for column, data_type in table["columns"].items():
            print(f"  {column}: {data_type}")

        print("Rows:", table["row_count"])

    def list_indexes(self):
        for name, index in self.indexes.items():
            print(
                f"{name}: "
                f"{index['table']}({index['column']})"
            )


catalog = SystemCatalog()

catalog.create_table(
    "employees",
    {
        "id": "INT",
        "name": "VARCHAR",
        "salary": "INT",
        "department": "VARCHAR"
    }
)

catalog.create_table(
    "departments",
    {
        "id": "INT",
        "name": "VARCHAR"
    }
)

catalog.add_rows("employees", 100)
catalog.add_rows("departments", 5)

catalog.create_index(
    "idx_employee_id",
    "employees",
    "id"
)

catalog.create_index(
    "idx_employee_department",
    "employees",
    "department"
)

print("Tables:")
print(catalog.list_tables())

catalog.describe_table("employees")

print("\nIndexes:")
catalog.list_indexes()

print("\nSchema:")
print(catalog.get_table_schema("employees"))