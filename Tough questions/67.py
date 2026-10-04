# Volcano Vectorized Execution Engine

class Operator:
    def open(self):
        pass

    def next_batch(self):
        raise StopIteration

    def close(self):
        pass


class TableScan(Operator):
    def __init__(self, table, batch_size=3):
        self.table = table
        self.batch_size = batch_size
        self.index = 0

    def open(self):
        self.index = 0

    def next_batch(self):
        if self.index >= len(self.table):
            raise StopIteration

        batch = self.table[
            self.index:self.index + self.batch_size
        ]

        self.index += self.batch_size

        return batch

    def close(self):
        pass


class Selection(Operator):
    def __init__(self, child, predicate):
        self.child = child
        self.predicate = predicate

    def open(self):
        self.child.open()

    def next_batch(self):
        while True:
            try:
                batch = self.child.next_batch()
            except StopIteration:
                raise

            result = [
                row
                for row in batch
                if self.predicate(row)
            ]

            if result:
                return result

    def close(self):
        self.child.close()


class Projection(Operator):
    def __init__(self, child, columns):
        self.child = child
        self.columns = columns

    def open(self):
        self.child.open()

    def next_batch(self):
        batch = self.child.next_batch()

        return [
            {
                column: row[column]
                for column in self.columns
            }
            for row in batch
        ]

    def close(self):
        self.child.close()


employees = [
    {"id": 1, "name": "Aman", "salary": 45000},
    {"id": 2, "name": "Rahul", "salary": 70000},
    {"id": 3, "name": "Priya", "salary": 60000},
    {"id": 4, "name": "Neha", "salary": 40000},
    {"id": 5, "name": "Ravi", "salary": 80000},
    {"id": 6, "name": "Anjali", "salary": 55000},
    {"id": 7, "name": "Karan", "salary": 30000},
]


scan = TableScan(employees, batch_size=3)

selection = Selection(
    scan,
    lambda row: row["salary"] >= 50000
)

projection = Projection(
    selection,
    ["name", "salary"]
)

projection.open()

while True:
    try:
        batch = projection.next_batch()
        print("Batch:", batch)
    except StopIteration:
        break

projection.close()