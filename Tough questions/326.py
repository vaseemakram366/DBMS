# Deadlock Prevention Algorithm


class DeadlockPrevention:
    def __init__(self):
        self.resource_order = {
            "R1": 1,
            "R2": 2,
            "R3": 3
        }

    def request_resources(self, transaction, resources):
        order = [self.resource_order[r] for r in resources]

        if order != sorted(order):
            print(f"{transaction}: Request Denied!")
            print("Resources must follow increasing order.")
        else:
            print(f"{transaction}: Request Approved!")

            for resource in resources:
                print(f"  Allocated {resource}")


obj = DeadlockPrevention()

obj.request_resources("T1", ["R1", "R2"])
obj.request_resources("T2", ["R3", "R1"])
