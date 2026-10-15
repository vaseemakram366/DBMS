# Database Index Recommendation Engine


from dataclasses import dataclass


@dataclass
class QueryWorkload:
    table: str
    columns: tuple
    executions: int
    rows_scanned: int
    rows_returned: int


class IndexRecommendationEngine:
    def __init__(self):
        self.workloads = []
        self.existing_indexes = set()
        self.write_rates = {}

    def add_existing_index(self, table, columns):
        self.existing_indexes.add((table, tuple(columns)))

    def set_write_rate(self, table, writes_per_hour):
        if writes_per_hour < 0:
            raise ValueError("Write rate cannot be negative")
        self.write_rates[table] = writes_per_hour

    def record_workload(
        self, table, columns, executions,
        rows_scanned, rows_returned
    ):
        if executions < 0 or rows_scanned < 0 or rows_returned < 0:
            raise ValueError("Workload values cannot be negative")

        if rows_returned > rows_scanned:
            raise ValueError("Returned rows cannot exceed scanned rows")

        self.workloads.append(
            QueryWorkload(
                table=table,
                columns=tuple(columns),
                executions=executions,
                rows_scanned=rows_scanned,
                rows_returned=rows_returned
            )
        )

    def recommend(self):
        candidates = {}

        for query in self.workloads:
            key = (query.table, query.columns)

            if key in self.existing_indexes:
                continue

            if query.rows_scanned == 0:
                continue

            scan_fraction = (
                query.rows_scanned - query.rows_returned
            ) / query.rows_scanned

            benefit = query.executions * scan_fraction
            candidates[key] = candidates.get(key, 0) + benefit

        results = []

        for (table, columns), benefit in candidates.items():
            write_rate = self.write_rates.get(table, 0)

            # Illustrative score, not a real optimizer cost model.
            penalty = write_rate * 0.01
            score = benefit - penalty

            if score > 0:
                results.append({
                    "table": table,
                    "columns": columns,
                    "benefit": benefit,
                    "write_rate": write_rate,
                    "score": score
                })

        return sorted(
            results,
            key=lambda item: item["score"],
            reverse=True
        )

    def report(self):
        recommendations = self.recommend()

        print("===== Index Recommendations =====")

        if not recommendations:
            print("No index recommendations found.")
            return

        for item in recommendations:
            columns = ", ".join(item["columns"])
            print(f"\nTable: {item['table']}")
            print(f"Suggested index columns: ({columns})")
            print(f"Estimated workload benefit: {item['benefit']:.2f}")
            print(f"Writes per hour: {item['write_rate']}")
            print(f"Recommendation score: {item['score']:.2f}")

        print("\nReview query plans before creating indexes.")


engine = IndexRecommendationEngine()

engine.add_existing_index("users", ("email",))

engine.set_write_rate("orders", 100)
engine.set_write_rate("users", 20)

engine.record_workload(
    "orders", ("customer_id",),
    executions=1000,
    rows_scanned=10000,
    rows_returned=10
)

engine.record_workload(
    "orders", ("status",),
    executions=400,
    rows_scanned=5000,
    rows_returned=500
)

engine.record_workload(
    "users", ("email",),
    executions=800,
    rows_scanned=2000,
    rows_returned=1
)

engine.report()
