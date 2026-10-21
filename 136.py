# Database Lock Audit Anomaly Detector


from collections import defaultdict


class LockAuditAnomalyDetector:
    def __init__(self, audit_log, denial_threshold=3):
        self.audit_log = audit_log
        self.denial_threshold = denial_threshold

    def detect_anomalies(self):
        denied_requests = defaultdict(int)
        rejected_releases = defaultdict(int)

        for event in self.audit_log:
            tx_id = event["transaction"]
            action = event["action"]
            status = event["status"]

            if action == "LOCK_DENIED":
                denied_requests[tx_id] += 1

            elif action == "RELEASE_REJECTED":
                rejected_releases[tx_id] += 1

        anomalies = []

        for tx_id, count in denied_requests.items():
            if count >= self.denial_threshold:
                anomalies.append(
                    f"{tx_id}: {count} lock requests denied"
                )

        for tx_id, count in rejected_releases.items():
            if count > 0:
                anomalies.append(
                    f"{tx_id}: {count} unauthorized release attempts"
                )

        return anomalies


audit_log = [
    {"transaction": "T1", "action": "LOCK_GRANTED",
     "status": "SUCCESS"},
    {"transaction": "T2", "action": "LOCK_DENIED",
     "status": "BLOCKED_BY:T1"},
    {"transaction": "T2", "action": "LOCK_DENIED",
     "status": "BLOCKED_BY:T1"},
    {"transaction": "T2", "action": "LOCK_DENIED",
     "status": "BLOCKED_BY:T1"},
    {"transaction": "T3", "action": "RELEASE_REJECTED",
     "status": "NOT_OWNER"}
]

detector = LockAuditAnomalyDetector(audit_log)
anomalies = detector.detect_anomalies()

print("LOCK AUDIT ANOMALY REPORT")
print("-" * 40)

if anomalies:
    for anomaly in anomalies:
        print(anomaly)
else:
    print("No anomalies detected")
