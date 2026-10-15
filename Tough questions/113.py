# Database Slow Query Detector


from collections import defaultdict


class SlowQueryDetector:
    def __init__(self, threshold_ms=500, frequent_limit=3):
        if threshold_ms < 0 or frequent_limit < 1:
            raise ValueError("Invalid detector configuration")

        self.threshold_ms = threshold_ms
        self.frequent_limit = frequent_limit
        self.query_stats = defaultdict(
            lambda: {"count": 0, "total_ms": 0, "max_ms": 0}
        )

    def record_query(self, query, execution_time_ms):
        if execution_time_ms < 0:
            raise ValueError("Execution time cannot be negative")

        stats = self.query_stats[query]
        stats["count"] += 1
        stats["total_ms"] += execution_time_ms
        stats["max_ms"] = max(stats["max_ms"], execution_time_ms)

    def analyze(self):
        results = []

        for query, stats in self.query_stats.items():
            average_ms = stats["total_ms"] / stats["count"]

            slow = stats["max_ms"] > self.threshold_ms
            frequent = stats["count"] >= self.frequent_limit

            if slow and frequent:
                priority = "HIGH"
            elif slow or frequent:
                priority = "MEDIUM"
            else:
                priority = "LOW"

            results.append({
                "query": query,
                "count": stats["count"],
                "average_ms": average_ms,
                "max_ms": stats["max_ms"],
                "priority": priority
            })

        return sorted(
            results,
            key=lambda item: (
                {"HIGH": 0, "MEDIUM": 1, "LOW": 2}[item["priority"]],
                -item["max_ms"]
            )
        )

    def report(self):
        results = self.analyze()

        print("===== Slow Query Analysis =====")

        if not results:
            print("No queries recorded.")
            return

        for item in results:
            print(f"\nQuery: {item['query']}")
            print(f"Executions: {item['count']}")
            print(f"Average time: {item['average_ms']:.2f} ms")
            print(f"Maximum time: {item['max_ms']:.2f} ms")
            print(f"Priority: {item['priority']}")


detector = SlowQueryDetector(
    threshold_ms=500,
    frequent_limit=3
)

detector.record_query("SELECT * FROM users", 20)
detector.record_query("SELECT * FROM users", 30)

detector.record_query("SELECT * FROM orders", 850)
detector.record_query("SELECT * FROM orders", 900)
detector.record_query("SELECT * FROM orders", 700)

detector.record_query("SELECT * FROM payments", 650)

detector.report()
