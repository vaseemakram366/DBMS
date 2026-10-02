# Columnar Storage Engine

class Column:
    def __init__(self, name):
        self.name = name
        self.values = []

    def append(self, value):
        self.values.append(value)

    def get(self, index):
        return self.values[index]


class ColumnarTable:
    def __init__(self, columns):
        self.columns = {
            name: Column(name)
            for name in columns
        }

        self.row_count = 0

    def insert(self, row):
        for column_name in self.columns:
            if column_name not in row:
                raise ValueError(
                    f"Missing column: {column_name}"
                )

            self.columns[column_name].append(
                row[column_name]
            )

        self.row_count += 1

    def scan_column(self, column_name):
        if column_name not in self.columns:
            raise ValueError("Column not found")

        return self.columns[column_name].values

    def filter(self, column_name, condition):
        if column_name not in self.columns:
            raise ValueError("Column not found")

        matching_rows = []

        column = self.columns[column_name]

        for index, value in enumerate(column.values):
            if condition(value):
                row = {}

                for name, col in self.columns.items():
                    row[name] = col.get(index)

                matching_rows.append(row)

        return matching_rows

    def aggregate_sum(self, column_name):
        return sum(
            self.scan_column(column_name)
        )

    def aggregate_avg(self, column_name):
        values = self.scan_column(column_name)

        if not values:
            return 0

        return sum(values) / len(values)

    def group_by_sum(self, group_column, value_column):
        result = {}

        groups = self.scan_column(group_column)
        values = self.scan_column(value_column)

        for group, value in zip(groups, values):
            result[group] = (
                result.get(group, 0) + value
            )

        return result

    def display_storage(self):
        print("\nColumnar Storage")
        print("-" * 40)

        for name, column in self.columns.items():
            print(
                f"{name}: {column.values}"
            )


if __name__ == "__main__":
    table = ColumnarTable([
        "id",
        "name",
        "department",
        "salary"
    ])

    table.insert({
        "id": 1,
        "name": "Aman",
        "department": "IT",
        "salary": 50000
    })

    table.insert({
        "id": 2,
        "name": "Rahul",
        "department": "HR",
        "salary": 60000
    })

    table.insert({
        "id": 3,
        "name": "Priya",
        "department": "IT",
        "salary": 70000
    })

    table.insert({
        "id": 4,
        "name": "Neha",
        "department": "Sales",
        "salary": 45000
    })

    table.display_storage()

    print("\nSalary Column:")
    print(table.scan_column("salary"))

    print("\nTotal Salary:")
    print(table.aggregate_sum("salary"))

    print("\nAverage Salary:")
    print(table.aggregate_avg("salary"))

    print("\nEmployees with salary >= 60000:")

    result = table.filter(
        "salary",
        lambda salary: salary >= 60000
    )

    for row in result:
        print(row)

    print("\nDepartment-wise Salary:")

    result = table.group_by_sum(
        "department",
        "salary"
    )

    for department, salary in result.items():
        print(department, salary)