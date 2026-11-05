# Two-Phase Commit Protocol


class TwoPhaseCommit:
    def __init__(self):
        self.servers = {
            "Server A": True,
            "Server B": True,
            "Server C": True
        }

    def execute_transaction(self):
        print("Phase 1: Prepare")

        all_ready = True

        for server, ready in self.servers.items():
            if ready:
                print(server, "voted YES")
            else:
                print(server, "voted NO")
                all_ready = False

        print("\nPhase 2: Decision")

        if all_ready:
            print("Transaction COMMITTED")
        else:
            print("Transaction ABORTED")


db = TwoPhaseCommit()
db.execute_transaction()
