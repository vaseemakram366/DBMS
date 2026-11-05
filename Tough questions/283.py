# Quorum-Based Replication


class QuorumReplication:
    def __init__(self):
        self.replicas = ["A", "B", "C"]
        self.N = 3
        self.R = 2
        self.W = 2

    def check_quorum(self):
        print("Total Replicas:", self.N)
        print("Read Quorum:", self.R)
        print("Write Quorum:", self.W)

        if self.R + self.W > self.N:
            print("Quorum condition satisfied")
            print("Read and Write operations allowed")
        else:
            print("Quorum condition not satisfied")

db = QuorumReplication()
db.check_quorum()
