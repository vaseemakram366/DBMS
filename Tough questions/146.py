# Banker's Algorithm — Deadlock Avoidance


class BankersAlgorithm:
    def __init__(self, available, maximum, allocation):
        self.available = available[:]
        self.maximum = maximum
        self.allocation = allocation
        self.n = len(allocation)
        self.m = len(available)

        self.need = [
            [
                maximum[i][j] - allocation[i][j]
                for j in range(self.m)
            ]
            for i in range(self.n)
        ]

    def safe_sequence(self):
        work = self.available[:]
        finished = [False] * self.n
        sequence = []

        while len(sequence) < self.n:
            progress = False

            for i in range(self.n):
                if finished[i]:
                    continue

                # Can this process finish with available resources?
                if all(self.need[i][j] <= work[j]
                       for j in range(self.m)):

                    # Process finishes and returns its allocated resources
                    for j in range(self.m):
                        work[j] += self.allocation[i][j]

                    finished[i] = True
                    sequence.append(i)
                    progress = True

            if not progress:
                return None

        return sequence

    def request_resources(self, process, request):
        if any(request[j] > self.need[process][j]
               for j in range(self.m)):
            print("Error: request exceeds declared maximum need")
            return False

        if any(request[j] > self.available[j]
               for j in range(self.m)):
            print("Request denied: resources currently unavailable")
            return False

        # Temporarily allocate requested resources
        for j in range(self.m):
            self.available[j] -= request[j]
            self.allocation[process][j] += request[j]
            self.need[process][j] -= request[j]

        sequence = self.safe_sequence()

        if sequence is None:
            # Unsafe state: undo temporary allocation
            for j in range(self.m):
                self.available[j] += request[j]
                self.allocation[process][j] -= request[j]
                self.need[process][j] += request[j]

            print("Request denied: system would become unsafe")
            return False

        print("Request granted")
        print("Safe sequence:", " -> ".join(f"P{i}" for i in sequence))
        return True


# Example: 5 processes, 3 resource types
available = [3, 3, 2]

maximum = [
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3]
]

allocation = [
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2]
]

bank = BankersAlgorithm(available, maximum, allocation)

print("Checking initial state...")
sequence = bank.safe_sequence()

if sequence is not None:
    print("System is SAFE")
    print("Safe sequence:", " -> ".join(f"P{i}" for i in sequence))
else:
    print("System is UNSAFE")

print("\nRequest: P1 asks for [1, 0, 2]")
bank.request_resources(1, [1, 0, 2])
