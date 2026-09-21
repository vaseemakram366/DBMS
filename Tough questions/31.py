# Two-Phase Commit (2PC) Protocol

class Participant:
    def __init__(self, name):
        self.name = name
        self.prepared = False
        self.committed = False
        self.aborted = False

    def prepare(self, transaction):
        if self.aborted:
            return False

        print(f"{self.name}: PREPARE {transaction}")
        self.prepared = True
        return True

    def commit(self, transaction):
        if not self.prepared:
            return False

        print(f"{self.name}: COMMIT {transaction}")
        self.committed = True
        return True

    def abort(self, transaction):
        print(f"{self.name}: ABORT {transaction}")
        self.aborted = True
        self.prepared = False


class Coordinator:
    def __init__(self, participants):
        self.participants = participants

    def execute(self, transaction):
        print(f"\nTransaction {transaction} started")

        votes = []

        for participant in self.participants:
            vote = participant.prepare(transaction)
            votes.append(vote)

        if all(votes):
            print("\nCoordinator: GLOBAL COMMIT")

            for participant in self.participants:
                participant.commit(transaction)

            return "COMMITTED"

        print("\nCoordinator: GLOBAL ABORT")

        for participant in self.participants:
            participant.abort(transaction)

        return "ABORTED"


node1 = Participant("Database-1")
node2 = Participant("Database-2")
node3 = Participant("Database-3")

coordinator = Coordinator([
    node1,
    node2,
    node3
])

result = coordinator.execute("T1001")

print("\nFinal Result:", result)