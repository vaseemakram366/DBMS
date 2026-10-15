# Database Query Latency Percentile Analyzer


class QueryLatencyAnalyzer:
    def __init__(self):
        self.latencies = []

    def record_query(self, latency_ms):
        if latency_ms < 0:
            raise ValueError("Latency cannot be negative")

        self.latencies.append(latency_ms)

    def percentile(self, p):
        if not 0 <= p <= 100:
            raise ValueError("Percentile must be between 0 and 100")

        if not self.latencies:
            return None

        values = sorted(self.latencies)

        # Nearest-rank percentile method
        rank = max(1, int((p / 100) * len(values) + 0.999999))
        return values[rank - 1]

    def report(self):
        if not self.latencies:
            print("No query latency data available.")
            return

        total = len(self.latencies)
        average = sum(self.latencies) / total

        print("===== Query Latency Report =====")
        print(f"Total queries: {total}")
        print(f"Minimum latency: {min(self.latencies):.2f} ms")
        print(f"Maximum latency: {max(self.latencies):.2f} ms")
        print(f"Average latency: {average:.2f} ms")
        print(f"P50 latency: {self.percentile(50):.2f} ms")
        print(f"P95 latency: {self.percentile(95):.2f} ms")
        print(f"P99 latency: {self.percentile(99):.2f} ms")


analyzer = QueryLatencyAnalyzer()

query_times = [
    10, 12, 15, 18, 20,
    22, 25, 28, 30, 35,
    40, 45, 50, 60, 80,
    100, 120, 150, 200, 500
]

for latency in query_times:
    analyzer.record_query(latency)

analyzer.report()
