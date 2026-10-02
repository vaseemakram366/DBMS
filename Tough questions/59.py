# Raft Consensus-Based Replicated Log

from dataclasses import dataclass


@dataclass
class LogEntry:
    term: int
    command: str


class RaftNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.current_term = 0
        self.state = "FOLLOWER"
        self.log = []
        self.commit_index = -1
        self.voted_for = None

    def become_candidate(self):
        self.state = "CANDIDATE"
        self.current_term += 1
        self.voted_for = self.node_id

        print(
            f"Node {self.node_id} became CANDIDATE "
            f"for term {self.current_term}"
        )

    def become_leader(self):
        self.state = "LEADER"

        print(
            f"Node {self.node_id} became LEADER "
            f"for term {self.current_term}"
        )

    def append_entry(self, command):
        if self.state != "LEADER":
            print(
                f"Node {self.node_id} rejected command: "
                f"not leader"
            )
            return

        entry = LogEntry(
            self.current_term,
            command
        )

        self.log.append(entry)

        print(
            f"Leader {self.node_id} appended: "
            f"{command}"
        )

    def receive_entries(self, entries, leader_term):
        if leader_term < self.current_term:
            return False

        self.current_term = leader_term
        self.state = "FOLLOWER"

        self.log = [
            LogEntry(entry.term, entry.command)
            for entry in entries
        ]

        return True

    def commit(self):
        if not self.log:
            return

        self.commit_index = len(self.log) - 1

    def show_log(self):
        print(
            f"\nNode {self.node_id} "
            f"[{self.state}]"
        )

        for index, entry in enumerate(self.log):
            status = (
                "COMMITTED"
                if index <= self.commit_index
                else "UNCOMMITTED"
            )

            print(
                f"{index}: "
                f"term={entry.term}, "
                f"command={entry.command}, "
                f"{status}"
            )


class RaftCluster:
    def __init__(self, node_count):
        self.nodes = [
            RaftNode(i)
            for i in range(node_count)
        ]

        self.leader = None

    def elect_leader(self, node_id):
        candidate = self.nodes[node_id]

        candidate.become_candidate()

        votes = 0

        for node in self.nodes:
            if node.current_term <= candidate.current_term:
                votes += 1

        majority = len(self.nodes) // 2 + 1

        if votes >= majority:
            candidate.become_leader()
            self.leader = candidate

    def replicate(self):
        if not self.leader:
            return

        for node in self.nodes:
            if node is not self.leader:
                node.receive_entries(
                    self.leader.log,
                    self.leader.current_term
                )

        self.leader.commit()

        for node in self.nodes:
            node.commit()

    def show_cluster(self):
        for node in self.nodes:
            node.show_log()


if __name__ == "__main__":
    cluster = RaftCluster(5)

    cluster.elect_leader(0)

    leader = cluster.leader

    leader.append_entry(
        "SET user:1 = Aman"
    )

    leader.append_entry(
        "SET balance:1 = 5000"
    )

    leader.append_entry(
        "SET status:1 = ACTIVE"
    )

    cluster.replicate()

    cluster.show_cluster()