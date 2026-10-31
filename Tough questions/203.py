# Two-Phase Commit (2PC) Simulator in Python


class Participant:
    def __init__(self, name, can_commit=True):
        self.name = name
        self.can_commit = can_commit
        self.state = "INITIAL"

    def prepare(self):
        if self.can_commit:
            self.state = "PREPARED"
            print(f"{self.name} votes YES")
            return True

        self.state = "ABORTED"
        print(f"{self.name} votes NO")
        return False

    def commit(self):
        self.state = "COMMITTED"
        print(f"{self.name} commits transaction")

    def abort(self):
        self.state = "ABORTED"
        print(f"{self.name} aborts transaction")


class TwoPhaseCommit:
    def __init__(self, participants):
        self.participants = participants

    def execute(self):
        print("Phase 1: PREPARE")

        votes = [
            participant.prepare()
            for participant in self.participants
        ]

        print("\nPhase 2: DECISION")

        if all(votes):
            print("Coordinator decision: COMMIT")

            for participant in self.participants:
                participant.commit()
        else:
            print("Coordinator decision: ABORT")

            for participant in self.participants:
                participant.abort()

        print("\nFinal participant states:")

        for participant in self.participants:
            print(f"{participant.name}: {participant.state}")


participants = [
    Participant("Database-A", can_commit=True),
    Participant("Database-B", can_commit=True),
    Participant("Database-C", can_commit=False)
]

coordinator = TwoPhaseCommit(participants)
coordinator.execute()
