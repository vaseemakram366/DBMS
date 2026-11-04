# Distributed Heartbeat Monitoring


class HeartbeatMonitor:
    def __init__(self, servers):
        self.servers = servers
        self.heartbeats = {
            server: True for server in servers
        }

    def receive_heartbeat(self, server):
        self.heartbeats[server] = True
        print(f"Heartbeat received from {server}")

    def mark_failed(self, server):
        self.heartbeats[server] = False

    def check_servers(self):
        for server, active in self.heartbeats.items():
            if active:
                print(f"{server}: ACTIVE")
            else:
                print(f"{server}: FAILED")


monitor = HeartbeatMonitor([
    "Server A",
    "Server B",
    "Server C"
])

monitor.receive_heartbeat("Server A")
monitor.receive_heartbeat("Server B")

monitor.mark_failed("Server C")

monitor.check_servers()
