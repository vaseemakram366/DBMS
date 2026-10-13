# Database Workload Anomaly Detector


from collections import defaultdict
from statistics import mean, pstdev


class WorkloadAnomalyDetector:
    def __init__(self, threshold=3):
        self.threshold = threshold
        self.execution_times = defaultdict(list)

    def record_query(self, fingerprint, execution_time):
        if execution_time < 0:
            raise ValueError("Execution time cannot be negative")

        history = self.execution_times[fingerprint]

        if len(history) >= 5:
            avg = mean(history)
            deviation = pstdev(history)

            if deviation == 0:
                is_anomaly = execution_time != avg
            else:
                z_score = abs((execution_time - avg) / deviation)
                is_anomaly = z_score > self.threshold

            if is_anomaly:
                print(
                    f"ANOMALY: {fingerprint} "
                    f"took {execution_time} ms"
                )
                print(f"Historical average: {avg:.2f} ms")
            else:
                print(
                    f"NORMAL: {fingerprint} "
                    f"took {execution_time} ms"
                )
        else:
            print(
                f"LEARNING: {fingerprint} "
                f"took {execution_time} ms"
            )

        history.append(execution_time)

    def report(self):
        print("\n--- Workload Report ---")

        for fingerprint, times in self.execution_times.items():
            print(f"Query: {fingerprint}")
            print(f"Executions: {len(times)}")
            print(f"Average: {mean(times):.2f} ms")
            print(f"Maximum: {max(times):.2f} ms")
            print()


detector = WorkloadAnomalyDetector(threshold=3)

query = "SELECT * FROM users WHERE id = ?"

for time_ms in [20, 21, 19, 20, 22, 21, 20, 500]:
    detector.record_query(query, time_ms)

detector.report()
