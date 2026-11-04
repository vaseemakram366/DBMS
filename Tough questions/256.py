# Database Failover Simulator


class DatabaseServer:
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.active = True


class FailoverManager:
    def __init__(self):
        self.primary = DatabaseServer("Server A", "Primary")
        self.replica = DatabaseServer("Server B", "Replica")

    def fail_primary(self):
        self.primary.active = False
        print("Primary server failed")

        if self.replica.active:
            self.replica.role = "Primary"
            print(f"{self.replica.name} promoted to Primary")
        else:
            print("No active replica available")

    def show_status(self):
        print(
            self.primary.name,
            "-", self.primary.role,
            "-", "Active" if self.primary.active else "Failed"
        )

        print(
            self.replica.name,
            "-", self.replica.role,
            "-", "Active" if self.replica.active else "Failed"
        )


manager = FailoverManager()

print("Before failure:")
manager.show_status()

print("\nAfter failure:")
manager.fail_primary()
manager.show_status()
