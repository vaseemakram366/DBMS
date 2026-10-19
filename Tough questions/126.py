# Transaction Starvation Detector


from time import time


class TransactionStarvationDetector:

    def __init__(self, max_wait_seconds=10, max_retries=3):
        self.max_wait_seconds = max_wait_seconds
        self.max_retries = max_retries
        self.transactions = {}

    def register_transaction(self, tx_id):
        self.transactions[tx_id] = {
            "start_time": time(),
            "retries": 0,
            "status": "WAITING"
        }

    def record_retry(self, tx_id):
        if tx_id in self.transactions:
            self.transactions[tx_id]["retries"] += 1

    def mark_completed(self, tx_id):
        if tx_id in self.transactions:
            self.transactions[tx_id]["status"] = "COMPLETED"

    def analyze(self):
        current_time = time()
        alerts = []

        for tx_id, tx in self.transactions.items():
            if tx["status"] != "WAITING":
                continue

            wait_time = current_time - tx["start_time"]

            if (
                wait_time >= self.max_wait_seconds
                or tx["retries"] >= self.max_retries
            ):
                alerts.append({
                    "transaction": tx_id,
                    "wait_seconds": wait_time,
                    "retries": tx["retries"]
                })

        return alerts

    def display_report(self):
        alerts = self.analyze()

        print("TRANSACTION STARVATION REPORT")
        print("-" * 40)

        if not alerts:
            print("No starvation risks detected.")
            return

        for alert in alerts:
            print(f"Transaction: {alert['transaction']}")
            print(f"Wait time: {alert['wait_seconds']:.2f} seconds")
            print(f"Retry count: {alert['retries']}")
            print("Status: STARVATION RISK")
            print()


detector = TransactionStarvationDetector(
    max_wait_seconds=10,
    max_retries=3
)

detector.register_transaction("T1")
detector.register_transaction("T2")
detector.register_transaction("T3")

detector.record_retry("T1")
detector.record_retry("T1")
detector.record_retry("T1")

detector.record_retry("T2")

detector.mark_completed("T3")

detector.display_report()
