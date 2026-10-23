# Transaction Starvation Prevention Manager


import heapq


class StarvationPreventionManager:
    def __init__(self, aging_interval=5):
        self.aging_interval = aging_interval
        self.current_time = 0
        self.sequence = 0
        self.waiting = []
        self.transactions = {}

    def add_transaction(self, tx, base_priority):
        if tx in self.transactions:
            print(f"{tx} already exists")
            return

        self.transactions[tx] = {
            "base_priority": base_priority,
            "arrival_time": self.current_time,
            "status": "WAITING"
        }

        self.sequence += 1
        heapq.heappush(
            self.waiting,
            (self._priority(tx), self.sequence, tx)
        )

        print(f"{tx} entered queue with priority {base_priority}")

    def _priority(self, tx):
        data = self.transactions[tx]
        waited = self.current_time - data["arrival_time"]
        aging_bonus = waited // self.aging_interval

        # Smaller number means higher priority
        return data["base_priority"] - aging_bonus

    def advance_time(self, units=1):
        self.current_time += units
        print(f"\nTime advanced to {self.current_time}")

    def schedule_next(self):
        if not self.waiting:
            print("No waiting transactions")
            return None

        # Recalculate effective priorities because aging changes over time
        candidates = [
            (self._priority(tx), seq, tx)
            for _, seq, tx in self.waiting
            if self.transactions[tx]["status"] == "WAITING"
        ]

        if not candidates:
            self.waiting.clear()
            print("No waiting transactions")
            return None

        priority, seq, tx = min(candidates)
        self.waiting = [
            item for item in self.waiting
            if item[2] != tx
        ]
        heapq.heapify(self.waiting)

        self.transactions[tx]["status"] = "RUNNING"

        print(
            f"Scheduled {tx}: effective priority={priority}"
        )
        return tx


# Demonstration
scheduler = StarvationPreventionManager(aging_interval=5)

scheduler.add_transaction("T1", base_priority=10)
scheduler.add_transaction("T2", base_priority=3)
scheduler.add_transaction("T3", base_priority=7)

scheduler.advance_time(10)
scheduler.schedule_next()

scheduler.advance_time(10)
scheduler.schedule_next()

scheduler.schedule_next()
