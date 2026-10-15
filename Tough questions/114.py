# Database Query Cost Anomaly Detector


from collections import defaultdict, deque
from statistics import median


class QueryCostAnomalyDetector:
    def __init__(self, window_size=5, min_history=4, threshold=3.5):
        if window_size < 1 or min_history < 1 or threshold <= 0:
            raise ValueError("Invalid detector configuration")

        self.window_size = window_size
        self.min_history = min_history
        self.threshold = threshold
        self.history = defaultdict(
            lambda: deque(maxlen=self.window_size)
        )

    def record_cost(self, query_name, cost):
        if cost < 0:
            raise ValueError("Cost cannot be negative")

        previous = list(self.history[query_name])

        if len(previous) < self.min_history:
            status = "BASELINE"
            score = None
        else:
            center = median(previous)
            deviations = [abs(value - center) for value in previous]
            mad = median(deviations)

            if mad == 0:
                anomalous = cost != center
                score = float("inf") if anomalous else 0.0
            else:
                score = 0.6745 * abs(cost - center) / mad
                anomalous = score > self.threshold

            status = "ANOMALY" if anomalous else "NORMAL"

        # Add the current observation only after evaluating it.
        self.history[query_name].append(cost)

        return {
            "query": query_name,
            "cost": cost,
            "status": status,
            "score": score
        }

    def report(self, query_name, costs):
        print(f"===== Analysis: {query_name} =====")

        for cost in costs:
            result = self.record_cost(query_name, cost)
            score = result["score"]

            if score is None:
                score_text = "N/A"
            elif score == float("inf"):
                score_text = "infinity"
            else:
                score_text = f"{score:.2f}"

            print(
                f"Cost: {cost:>6} | "
                f"Status: {result['status']:<8} | "
                f"Score: {score_text}"
            )


detector = QueryCostAnomalyDetector(
    window_size=5,
    min_history=4,
    threshold=3.5
)

detector.report(
    "orders_lookup",
    [100, 102, 98, 101, 99, 105, 900]
)
