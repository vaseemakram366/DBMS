# Query Execution Engine with Selection, Projection & Sorting
class QueryEngine:

    def __init__(self, table):
        self.table = table

    def select(self, condition=None):
        if condition is None:
            return self.table[:]

        column, operator, value = condition
        result = []

        for row in self.table:
            current = row[column]

            if operator == "=" and current == value:
                result.append(row)

            elif operator == ">" and current > value:
                result.append(row)

            elif operator == "<" and current < value:
                result.append(row)

            elif operator == ">=" and current >= value:
                result.append(row)

            elif operator == "<=" and current <= value:
                result.append(row)

        return result

    def project(self, rows, columns):
        return [
            {column: row[column] for column in columns}
            for row in rows
        ]

    def sort(self, rows, column, reverse=False):
        return sorted(
            rows,
            key=lambda row: row[column],
            reverse=reverse
        )

    def execute(self, condition=None, columns=None,
                order_by=None, descending=False):

        rows = self.select(condition)

        if columns:
            rows = self.project(rows, columns)

        if order_by:
            rows = self.sort(
                rows,
                order_by,
                descending
            )

        return rows


students = [
    {"id": 1, "name": "Vaseem", "marks": 92},
    {"id": 2, "name": "Rahul", "marks": 78},
    {"id": 3, "name": "Aman", "marks": 95},
    {"id": 4, "name": "Sara", "marks": 88},
    {"id": 5, "name": "Karan", "marks": 67}
]

engine = QueryEngine(students)

result = engine.execute(
    condition=("marks", ">=", 80),
    columns=["name", "marks"],
    order_by="marks",
    descending=True
)

print("Query Result:")

for row in result:
    print(row)