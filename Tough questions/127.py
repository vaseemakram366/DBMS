# Fair Lock Queue Scheduler


from collections import deque


class FairLockQueueScheduler:

    def __init__(self):
        self.waiting_queue = deque()
        self.lock_owner = None

    def request_lock(self, transaction_id):
        if transaction_id == self.lock_owner:
            print(f"{transaction_id} already owns the lock.")
            return

        if transaction_id in self.waiting_queue:
            print(f"{transaction_id} is already waiting.")
            return

        if self.lock_owner is None and not self.waiting_queue:
            self.lock_owner = transaction_id
            print(f"Lock granted to {transaction_id}")
        else:
            self.waiting_queue.append(transaction_id)
            print(f"{transaction_id} added to waiting queue.")

    def release_lock(self, transaction_id):
        if transaction_id != self.lock_owner:
            print(f"{transaction_id} does not own the lock.")
            return

        print(f"{transaction_id} released the lock.")
        self.lock_owner = None

        if self.waiting_queue:
            next_transaction = self.waiting_queue.popleft()
            self.lock_owner = next_transaction
            print(f"Lock granted to {next_transaction}")

    def display_status(self):
        print("\nLOCK STATUS")
        print("Current owner:", self.lock_owner)
        print("Waiting queue:", list(self.waiting_queue))


scheduler = FairLockQueueScheduler()

scheduler.request_lock("T1")
scheduler.request_lock("T2")
scheduler.request_lock("T3")
scheduler.request_lock("T4")

scheduler.display_status()

print("\n--- Releasing locks ---")
scheduler.release_lock("T1")
scheduler.release_lock("T2")
scheduler.release_lock("T3")
scheduler.release_lock("T4")

scheduler.display_status()
