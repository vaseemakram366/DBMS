# Parallel Query Execution Scheduler

from concurrent.futures import ThreadPoolExecutor


class ParallelQueryExecutor:
    def __init__(self, workers=4):
        self.workers = workers

    def _process_chunk(self, rows, column, condition):
        result = []

        for row in rows:
            if condition(row[column]):
                result.append(row)

        return result

    def execute(self, rows, column, condition):
        chunk_size = (
            len(rows) + self.workers - 1
        ) // self.workers

        chunks = [
            rows[i:i + chunk_size]
            for i in range(0, len(rows), chunk_size)
        ]

        with ThreadPoolExecutor(
            max_workers=self.workers
        ) as executor:

            futures = [
                executor.submit(
                    self._process_chunk,
                    chunk,
                    column,
                    condition
                )
                for chunk in chunks
            ]

            results = [
                future.result()
                for future in futures
            ]

        return [
            row
            for result in results
            for row in result
        ]


class Database:
    def __init__(self):
        self.rows = []

    def insert(self, row):
        self.rows.append(row)

    def parallel_query(
        self,
        column,
        condition,
        workers=4
    ):
        executor = ParallelQueryExecutor(workers)

        return executor.execute(
            self.rows,
            column,
            condition
        )


db = Database()

for i in range(1, 21):
    db.insert({
        "id": i,
        "salary": i * 5000
    })

result = db.parallel_query(
    "salary",
    lambda salary: salary >= 50000,
    workers=4
)

for row in result:
    print(row)