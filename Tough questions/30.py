# Index Nested Loop Join

class IndexNestedLoopJoin:
    def __init__(self, inner_table, index_column):
        self.inner_table = inner_table
        self.index_column = index_column
        self.index = {}

        self.build_index()

    def build_index(self):
        for row in self.inner_table:
            key = row[self.index_column]
            self.index.setdefault(key, []).append(row)

    def join(self, outer_table, outer_column):
        result = []

        for outer_row in outer_table:
            key = outer_row[outer_column]

            if key in self.index:
                for inner_row in self.index[key]:
                    result.append(outer_row + inner_row)

        return result


employees = [
    (1, "Amit", 10),
    (2, "Rahul", 20),
    (3, "Vaseem", 10),
    (4, "Neha", 30),
    (5, "Arjun", 20)
]

departments = [
    (10, "CSE"),
    (20, "ECE"),
    (30, "ME")
]

joiner = IndexNestedLoopJoin(
    departments,
    0
)

result = joiner.join(
    employees,
    2
)

for row in result:
    print(row)