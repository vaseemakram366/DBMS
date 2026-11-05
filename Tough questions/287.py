# Optimistic Concurrency Control


class OptimisticConcurrencyControl:
    def __init__(self):
        self.balance = 1000
        self.version = 1

    def start_transaction(self):
        snapshot = {
            "balance": self.balance,
            "version": self.version
        }

        print("Transaction started:", snapshot)
        return snapshot

    def update_balance(self, transaction, new_balance):
        if transaction["version"] == self.version:
            self.balance = new_balance
            self.version += 1

            print("Transaction COMMITTED")
            print("Updated Balance:", self.balance)
        else:
            print("Transaction ABORTED: Conflict detected")


db = OptimisticConcurrencyControl()

t1 = db.start_transaction()
t2 = db.start_transaction()

db.update_balance(t1, 1500)
db.update_balance(t2, 2000)
