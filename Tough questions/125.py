# Database Deadlock Victim Selector


class DeadlockVictimSelector:

    def __init__(self):
        self.transactions = {}

    def add_transaction(
        self,
        tx_id,
        age_seconds,
        work_completed,
        rollback_cost
    ):
        self.transactions[tx_id] = {
            "age": age_seconds,
            "work": work_completed,
            "rollback_cost": rollback_cost
        }

    def select_victim(self, deadlock_cycle):
        candidates = deadlock_cycle[:-1]

        valid_candidates = [
            tx for tx in candidates
            if tx in self.transactions
        ]

        if not valid_candidates:
            return None

        def victim_score(tx_id):
            tx = self.transactions[tx_id]

            return (
                tx["rollback_cost"],
                tx["work"],
                -tx["age"]
            )

        return min(valid_candidates, key=victim_score)

    def display_victim(self, deadlock_cycle):
        print("DEADLOCK CYCLE:", " -> ".join(deadlock_cycle))

        victim = self.select_victim(deadlock_cycle)

        if victim is None:
            print("No valid victim found.")
            return

        tx = self.transactions[victim]

        print(f"\nSelected victim: {victim}")
        print(f"Rollback cost: {tx['rollback_cost']}")
        print(f"Work completed: {tx['work']}")
        print(f"Transaction age: {tx['age']} seconds")
        print(f"Action: Rollback {victim} to break the deadlock.")


selector = DeadlockVictimSelector()

selector.add_transaction("T1", 30, 80, 8)
selector.add_transaction("T2", 5, 10, 2)
selector.add_transaction("T3", 15, 40, 4)

cycle = ["T1", "T2", "T3", "T1"]

selector.display_victim(cycle)
