# Dirty Read, Non-repeatable Read and Phantom Read Simulator


class ConcurrencyAnomalySimulator:
    def __init__(self):
        self.committed_balance = 100
        self.pending_balance = None
        self.students = [
            {"id": 1, "marks": 80},
            {"id": 2, "marks": 90}
        ]

    def dirty_read_demo(self):
        print("\n--- Dirty Read ---")

        self.pending_balance = 200
        print("T1 writes balance = 200 (uncommitted)")

        print("T2 reads balance =", self.pending_balance)

        self.pending_balance = None
        print("T1 rolls back")

        print("Committed balance =", self.committed_balance)

    def non_repeatable_read_demo(self):
        print("\n--- Non-repeatable Read ---")

        first_read = self.committed_balance
        print("T2 first read =", first_read)

        self.committed_balance = 150
        print("T1 updates balance to 150 and commits")

        second_read = self.committed_balance
        print("T2 second read =", second_read)

    def phantom_read_demo(self):
        print("\n--- Phantom Read ---")

        first_result = [
            s for s in self.students if s["marks"] >= 85
        ]
        print("T2 first query =", first_result)

        self.students.append({"id": 3, "marks": 95})
        print("T1 inserts student with marks = 95 and commits")

        second_result = [
            s for s in self.students if s["marks"] >= 85
        ]
        print("T2 second query =", second_result)


db = ConcurrencyAnomalySimulator()

db.dirty_read_demo()
db.non_repeatable_read_demo()
db.phantom_read_demo()
