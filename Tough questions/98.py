# Paxos Consensus Algorithm


class Acceptor:
    def __init__(self, node_id):
        self.node_id = node_id
        self.promised_id = 0
        self.accepted_id = 0
        self.accepted_value = None

    def prepare(self, proposal_id):
        if proposal_id <= self.promised_id:
            return None

        self.promised_id = proposal_id

        return {
            "node": self.node_id,
            "accepted_id": self.accepted_id,
            "accepted_value": self.accepted_value
        }

    def accept(self, proposal_id, value):
        if proposal_id < self.promised_id:
            return False

        self.promised_id = proposal_id
        self.accepted_id = proposal_id
        self.accepted_value = value

        return True


class Proposer:
    def __init__(self, proposal_id, acceptors):
        self.proposal_id = proposal_id
        self.acceptors = acceptors

    def propose(self, value):
        majority = len(self.acceptors) // 2 + 1

        promises = []

        for acceptor in self.acceptors:
            response = acceptor.prepare(self.proposal_id)

            if response is not None:
                promises.append(response)

        if len(promises) < majority:
            print("Prepare phase failed")
            return None

        previously_accepted = [
            response for response in promises
            if response["accepted_value"] is not None
        ]

        if previously_accepted:
            highest = max(
                previously_accepted,
                key=lambda response: response["accepted_id"]
            )
            value = highest["accepted_value"]

        accepted_count = 0

        for acceptor in self.acceptors:
            if acceptor.accept(self.proposal_id, value):
                accepted_count += 1

        if accepted_count >= majority:
            print("Consensus reached:", value)
            return value

        print("Accept phase failed")
        return None


nodes = [
    Acceptor(1),
    Acceptor(2),
    Acceptor(3)
]

proposer = Proposer(1, nodes)
proposer.propose("TXN-101")

print("\nAcceptor states:")
for node in nodes:
    print(
        f"Node {node.node_id}: "
        f"proposal={node.accepted_id}, "
        f"value={node.accepted_value}"
    )


