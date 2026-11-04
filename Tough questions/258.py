# Raft Leader Election Basics


class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.state = "Follower"
        self.active = True
        self.votes = 0


class RaftCluster:
    def __init__(self, count):
        self.servers = [
            Server(i) for i in range(1, count + 1)
        ]

    def start_election(self):
        candidates = [
            s for s in self.servers if s.active
        ]

        if not candidates:
            print("No active servers available")
            return

        candidate = max(
            candidates,
            key=lambda s: s.server_id
        )

        candidate.state = "Candidate"
        candidate.votes = len(candidates)

        if candidate.votes > len(self.servers) // 2:
            for server in self.servers:
                server.state = "Follower"

            candidate.state = "Leader"
            print(f"Server {candidate.server_id} elected as Leader")
        else:
            print("Election failed: majority not reached")

    def show_status(self):
        for server in self.servers:
            status = "Active" if server.active else "Failed"
            print(
                f"Server {server.server_id}: "
                f"{server.state}, {status}"
            )


cluster = RaftCluster(3)

cluster.start_election()
cluster.show_status()
