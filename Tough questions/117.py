# Database Query Plan Regression Detector


from dataclasses import dataclass
from statistics import median


@dataclass
class PlanObservation:
    plan_name: str
    execution_ms: float
    rows_scanned: int


class QueryPlanRegressionDetector:
    def __init__(self, regression_threshold=1.5):
        if regression_threshold <= 1:
            raise ValueError("Threshold must be greater than 1")

        self.threshold = regression_threshold
        self.history = {}

    def record_plan(self, query_id, plan_name, execution_ms, rows_scanned):
        if execution_ms < 0 or rows_scanned < 0:
            raise ValueError("Metrics cannot be negative")

        self.history.setdefault(query_id, []).append(
            PlanObservation(plan_name, execution_ms, rows_scanned)
        )

    def analyze(self, query_id):
        observations = self.history.get(query_id, [])

        if len(observations) < 2:
            return {
                "status": "INSUFFICIENT DATA",
                "message": "Record at least two plan observations."
            }

        old_plan = observations[-2]
        new_plan = observations[-1]

        if old_plan.execution_ms == 0:
            ratio = (
                float("inf")
                if new_plan.execution_ms > 0
                else 1.0
            )
        else:
            ratio = new_plan.execution_ms / old_plan.execution_ms

        regressed = ratio >= self.threshold

        return {
            "query_id": query_id,
            "old_plan": old_plan.plan_name,
            "new_plan": new_plan.plan_name,
            "old_latency": old_plan.execution_ms,
            "new_latency": new_plan.execution_ms,
            "latency_ratio": ratio,
            "rows_scanned_change": (
                new_plan.rows_scanned - old_plan.rows_scanned
            ),
            "status": "REGRESSION" if regressed else "NORMAL"
        }

    def report(self, query_id):
        result = self.analyze(query_id)

        print("===== Query Plan Regression Report =====")

        for key, value in result.items():
            print(f"{key}: {value}")


detector = QueryPlanRegressionDetector(regression_threshold=1.5)

detector.record_plan(
    "Q101", "Index Scan", execution_ms=100, rows_scanned=500
)

detector.record_plan(
    "Q101", "Full Table Scan", execution_ms=280, rows_scanned=10000
)

detector.report("Q101")
