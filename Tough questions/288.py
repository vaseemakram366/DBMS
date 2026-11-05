# Pessimistic Concurrency Control


class PessimisticConcurrencyControl:
    def __init__(self):
        self.balance = 1000
        self.locked = False

    def acquire_lock(self, transaction):
        if not self.locked:
            self.locked = True
            print(transaction, "acquired lock")
            return True

        print(transaction, "cannot acquire lock")
        return False

    def update_balance(self, transaction, value):
        if self.acquire_lock(transaction):
            self.balance = value
            print("Balance updated:", self.balance)

            self.locked = False
            print(transaction, "released lock")


db = PessimisticConcurrencyControl()

db.update_balance("T1", 1500)
db.update_balance("T2", 2000)
