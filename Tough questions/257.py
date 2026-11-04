# Automatic Primary Server Election


class Server:
    def __init__(self, server_id):
        self.server_id = server_id
        self.active = True
        self.role = "Replica"


class LeaderElection:
    def __init__(self):
        self.servers = [
            Server(1),
            Server(2),
            Server(3)
        ]

    def fail_server(self, server_id):
        for server in self.servers:
            if server.server_id == server_id:
                server.active = False
                print(f"Server {server_id} failed")

    def elect_leader(self):
        active_servers = [
            server for server in self.servers
            if server.active
        ]

        if not active_servers:
            print("No active server available")
            return

        leader = max(
            active_servers,
            key=lambda server: server.server_id
        )

        for server in self.servers:
            server.role = "Replica"

        leader.role = "Primary"

        print(f"Server {leader.server_id} elected as Primary")

    def show_status(self):
        for server in self.servers:
            status = "Active" if server.active else "Failed"
            print(
                f"Server {server.server_id}: "
                f"{server.role}, {status}"
            )


cluster = LeaderElection()

cluster.fail_server(3)
cluster.elect_leader()
cluster.show_status()
