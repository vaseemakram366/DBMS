# Query Execution Engine

class Operator:
    def open(self):
        pass

    def next(self):
        raise StopIteration

    def close(self):
        pass


class TableScan(Operator):
    def __init__(self, table):
        self.table = table
        self.index = 0

    def open(self):
        self.index = 0

    def next(self):
        if self.index >= len(self.table):
            raise StopIteration

        row = self.table[self.index]
        self.index += 1
        return row

    def close(self):
        pass


class Selection(Operator):
    def __init__(self, child, predicate):
        self.child = child
        self.predicate = predicate

    def open(self):
        self.child.open()

    def next(self):
        while True:
            row = self.child.next()

            if self.predicate(row):
                return row

    def close(self):
        self.child.close()


class Projection(Operator):
    def __init__(self, child, columns):
        self.child = child
        self.columns = columns

    def open(self):
        self.child.open()

    def next(self):
        row = self.child.next()
        return {column: row[column] for column in self.columns}

    def close(self):
        self.child.close()


employees = [
    {"id": 1, "name": "Aman", "salary": 45000},
    {"id": 2, "name": "Rahul", "salary": 70000},
    {"id": 3, "name": "Priya", "salary": 60000},
    {"id": 4, "name": "Neha", "salary": 40000},
]

scan = TableScan(employees)

selection = Selection(
    scan,
    lambda row: row["salary"] > 50000
)

projection = Projection(
    selection,
    ["name", "salary"]
)

projection.open()

while True:
    try:
        print(projection.next())
    except StopIteration:
        break

projection.close()