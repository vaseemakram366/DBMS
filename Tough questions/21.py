class TransactionManager:

    def __init__(self):
        self.database = {}
        self.transactions = {}

    def create_account(self, account, balance):
        self.database[account] = balance

    def begin(self, tid):
        if tid in self.transactions:
            print("Transaction already exists")
            return

        self.transactions[tid] = {
            "status": "ACTIVE",
            "changes": []
        }

        print(tid, "started")

    def read(self, tid, account):
        if not self._active(tid):
            return None

        if account not in self.database:
            print("Account does not exist")
            return None

        value = self.database[account]

        print(
            tid,
            "READ",
            account,
            "=",
            value
        )

        return value

    def write(self, tid, account, amount):
        if not self._active(tid):
            return

        if account not in self.database:
            print("Account does not exist")
            return

        old_value = self.database[account]

        self.transactions[tid]["changes"].append(
            (account, old_value)
        )

        self.database[account] = amount

        print(
            tid,
            "WRITE",
            account,
            "=",
            amount
        )

    def commit(self, tid):
        if not self._active(tid):
            return

        self.transactions[tid]["status"] = "COMMITTED"

        print(tid, "COMMITTED")

    def rollback(self, tid):
        if not self._active(tid):
            return

        changes = self.transactions[tid]["changes"]

        for account, old_value in reversed(changes):
            self.database[account] = old_value

        self.transactions[tid]["status"] = "ROLLED BACK"

        print(tid, "ROLLED BACK")

    def transfer(self, tid, sender, receiver, amount):
        if not self._active(tid):
            return

        if sender not in self.database:
            print("Sender does not exist")
            return

        if receiver not in self.database:
            print("Receiver does not exist")
            return

        if self.database[sender] < amount:
            print("Insufficient balance")
            return

        sender_old = self.database[sender]
        receiver_old = self.database[receiver]

        self.transactions[tid]["changes"].append(
            (sender, sender_old)
        )

        self.transactions[tid]["changes"].append(
            (receiver, receiver_old)
        )

        self.database[sender] -= amount
        self.database[receiver] += amount

        print(
            tid,
            "TRANSFERRED",
            amount,
            "from",
            sender,
            "to",
            receiver
        )

    def _active(self, tid):
        if tid not in self.transactions:
            print("Transaction does not exist")
            return False

        if self.transactions[tid]["status"] != "ACTIVE":
            print("Transaction is not active")
            return False

        return True

    def show_database(self):
        print("\nDatabase:")

        for account, balance in self.database.items():
            print(account, "=", balance)


tm = TransactionManager()

tm.create_account("A", 10000)
tm.create_account("B", 5000)
tm.create_account("C", 2000)

tm.begin("T1")

tm.read("T1", "A")

tm.transfer(
    "T1",
    "A",
    "B",
    3000
)

tm.read("T1", "A")

tm.commit("T1")

tm.show_database()

tm.begin("T2")

tm.transfer(
    "T2",
    "B",
    "C",
    2000
)

tm.show_database()

tm.rollback("T2")

tm.show_database()