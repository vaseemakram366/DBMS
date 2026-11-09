# Banker's Algorithm for Deadlock Avoidance


class BankersAlgorithm:
    def __init__(self):
        self.available = [3, 3, 2]

        self.max_need = [
            [7, 5, 3],
            [3, 2, 2],
            [9, 0, 2],
            [2, 2, 2],
            [4, 3, 3]
        ]

        self.allocation = [
            [0, 1, 0],
            [2, 0, 0],
            [3, 0, 2],
            [2, 1, 1],
            [0, 0, 2]
        ]

    def check_safe_state(self):
        n = len(self.allocation)
        m = len(self.available)

        need = [
            [
                self.max_need[i][j] - self.allocation[i][j]
                for j in range(m)
            ]
            for i in range(n)
        ]

        work = self.available.copy()
        finish = [False] * n
        safe_sequence = []

        while len(safe_sequence) < n:
            found = False

            for i in range(n):
                if not finish[i] and all(
                    need[i][j] <= work[j] for j in range(m)
                ):
                    for j in range(m):
                        work[j] += self.allocation[i][j]

                    finish[i] = True
                    safe_sequence.append(i)
                    found = True

            if not found:
                print("System is NOT in a safe state!")
                return

        print("System is in a SAFE state.")
        print("Safe Sequence:", safe_sequence)


obj = BankersAlgorithm()
obj.check_safe_state()
