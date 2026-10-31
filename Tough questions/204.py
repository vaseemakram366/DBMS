# Three-Phase Commit (3PC) Simulator


class Participant:
    def __init__(self, name, ready=True):
        self.name = name
        self.ready = ready
        self.state = "INITIAL"

    def can_commit(self):
        if self.ready:
            self.state = "READY"
            print(f"{self.name}: YES")
            return True

        self.state = "ABORTED"
        print(f"{self.name}: NO")
        return False

    def pre_commit(self):
        self.state = "PRECOMMITTED"
        print(f"{self.name}: PRECOMMITTED")

    def do_commit(self):
        self.state = "COMMITTED"
        print(f"{self.name}: COMMITTED")

    def abort(self):
        self.state = "ABORTED"
        print(f"{self.name}: ABORTED")


class ThreePhaseCommit:
    def __init__(self, participants):
        self.participants = participants

    def execute(self):
        print("Phase 1: CAN-COMMIT")

        votes = [
            p.can_commit() for p in self.participants
        ]

        if not all(votes):
            print("Transaction ABORTED")
            for p in self.participants:
                p.abort()
            return

        print("\nPhase 2: PRE-COMMIT")

        for p in self.participants:
            p.pre_commit()

        print("\nPhase 3: DO-COMMIT")

        for p in self.participants:
            p.do_commit()

        print("\nAll participants committed successfully.")


participants = [
    Participant("Database-A"),
    Participant("Database-B"),
    Participant("Database-C")
]

ThreePhaseCommit(participants).execute()
