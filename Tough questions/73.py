# Query Result Streaming Engine

class QueryStream:
    def __init__(self, rows):
        self.rows = rows
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.rows):
            raise StopIteration

        row = self.rows[self.index]
        self.index += 1

        return row


class FilterStream:
    def __init__(self, source, predicate):
        self.source = source
        self.predicate = predicate

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            row = next(self.source)

            if self.predicate(row):
                return row


class ProjectStream:
    def __init__(self, source, columns):
        self.source = source
        self.columns = columns

    def __iter__(self):
        return self

    def __next__(self):
        row = next(self.source)

        return {
            column: row[column]
            for column in self.columns
        }


class LimitStream:
    def __init__(self, source, limit):
        self.source = source
        self.limit = limit
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.limit:
            raise StopIteration

        row = next(self.source)

        self.count += 1

        return row


employees = [
    {"id": 1, "name": "Aman", "salary": 45000},
    {"id": 2, "name": "Rahul", "salary": 80000},
    {"id": 3, "name": "Priya", "salary": 70000},
    {"id": 4, "name": "Neha", "salary": 40000},
    {"id": 5, "name": "Ravi", "salary": 90000},
    {"id": 6, "name": "Anjali", "salary": 85000},
    {"id": 7, "name": "Karan", "salary": 30000}
]


scan = QueryStream(employees)

filtered = FilterStream(
    scan,
    lambda row: row["salary"] >= 70000
)

projected = ProjectStream(
    filtered,
    ["name", "salary"]
)

limited = LimitStream(
    projected,
    3
)


for row in limited:
    print(row)