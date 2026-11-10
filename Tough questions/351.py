# Transaction Rollback Simulation


class Transaction:
    def __init__(self, balance):
        self.balance = balance
        self.old_balance = balance

    def withdraw(self, amount):
        self.balance -= amount
        print("After withdrawal:", self.balance)

    def rollback(self):
        self.balance = self.old_balance
        print("Transaction rolled back!")
        print("Final balance:", self.balance)


account = Transaction(1000)

print("Initial balance:", account.balance)

account.withdraw(200)

account.rollback()
