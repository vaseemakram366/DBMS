# Deadlock Victim Selection Engine


class DeadlockVictimSelector:
    def __init__(self):
        self.transactions = {}

    def add_transaction(self, tx, age, work_done, locks_held):
        self.transactions[tx] = {
            "age": age,
            "work_done": work_done,
            "locks_held": locks_held
        }

    def rollback_cost(self, tx):
        data = self.transactions[tx]

        # More completed work means more work may be lost.
        # Held locks add a small recovery penalty.
        return data["work_done"] + 5 * data["locks_held"]

    def select_victim(self, deadlocked_transactions):
        candidates = [
            tx for tx in deadlocked_transactions
            if tx in self.transactions
        ]

        if not candidates:
            print("No valid victim candidates")
            return None

        # Prefer the transaction with the lowest estimated cost.
        victim = min(
            candidates,
            key=lambda tx: (
                self.rollback_cost(tx),
                self.transactions[tx]["age"]
            )
        )

        print("\nDeadlock candidates:")
        for tx in candidates:
            data = self.transactions[tx]
            print(
                f"{tx}: work={data['work_done']}, "
                f"locks={data['locks_held']}, "
                f"estimated_cost={self.rollback_cost(tx)}"
            )

        print(f"\nSelected victim: {victim}")
        print(f"Estimated rollback cost: {self.rollback_cost(victim)}")

        return victim


# Demonstration
selector = DeadlockVictimSelector()

selector.add_transaction("T1", age=1, work_done=80, locks_held=3)
selector.add_transaction("T2", age=2, work_done=20, locks_held=1)
selector.add_transaction("T3", age=3, work_done=45, locks_held=2)

deadlock_cycle = ["T1", "T2", "T3"]

victim = selector.select_victim(deadlock_cycle)
