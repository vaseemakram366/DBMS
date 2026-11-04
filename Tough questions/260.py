# Database Server Health Checker


class DatabaseHealthChecker:
    def __init__(self, server_name, cpu, memory, connected):
        self.server_name = server_name
        self.cpu = cpu
        self.memory = memory
        self.connected = connected

    def check_health(self):
        print("Server:", self.server_name)

        if not self.connected:
            print("Status: UNHEALTHY")
            print("Reason: Database connection failed")
            return

        if self.cpu > 80 or self.memory > 80:
            print("Status: UNHEALTHY")
            print("Reason: High resource usage")
        else:
            print("Status: HEALTHY")

        print("CPU Usage:", self.cpu, "%")
        print("Memory Usage:", self.memory, "%")


server1 = DatabaseHealthChecker(
    "DB-Server-1", 45, 60, True
)

server2 = DatabaseHealthChecker(
    "DB-Server-2", 90, 50, True
)

server1.check_health()

print()

server2.check_health()
 