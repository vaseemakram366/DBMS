# CAP Theorem Simulator


class CAPTheorem:
    def __init__(self):
        self.partition = True

    def simulate(self):
        print("Network Partition:", self.partition)

        if self.partition:
            print("Consistency: Maintained")
            print("Availability: Reduced")
            print("System Type: CP")
        else:
            print("Consistency: Maintained")
            print("Availability: Maintained")
            print("System: Normal Operation")


db = CAPTheorem()
db.simulate()
