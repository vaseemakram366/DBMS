class OnlineIndex:
    def __init__(self, column):
        self.column = column
        self.index = {}
        self.pending = []
        self.building = True

    def _add_to_index(self, row):
        key = row[self.column]

        if key not in self.index:
            self.index[key] = []

        self.index[key].append(row)

    def insert(self, row):
        if self.building:
            self.pending.append(row)
        else:
            self._add_to_index(row)

    def build_batch(self, rows):
        for row in rows:
            self._add_to_index(row)

    def finish_build(self):
        for row in self.pending:
            self._add_to_index(row)

        self.pending.clear()
        self.building = False

    def search(self, value):
        return self.index.get(value, [])


class Database:
    def __init__(self):
        self.rows = []
        self.indexes = {}

    def insert(self, row):
        self.rows.append(row)

        for index in self.indexes.values():
            index.insert(row)

    def create_online_index(self, column):
        index = OnlineIndex(column)
        self.indexes[column] = index

        batch_size = 2

        for i in range(0, len(self.rows), batch_size):
            batch = self.rows[i:i + batch_size]
            index.build_batch(batch)

        index.finish_build()

    def search(self, column, value):
        if column not in self.indexes:
            return [
                row for row in self.rows
                if row[column] == value
            ]

        return self.indexes[column].search(value)


db = Database()

db.insert({
    "id": 1,
    "name": "Rahul",
    "department": "CSE"
})

db.insert({
    "id": 2,
    "name": "Aman",
    "department": "ECE"
})

db.insert({
    "id": 3,
    "name": "Vikas",
    "department": "CSE"
})

db.create_online_index("department")

db.insert({
    "id": 4,
    "name": "Arjun",
    "department": "CSE"
})

print(db.search("department", "CSE"))