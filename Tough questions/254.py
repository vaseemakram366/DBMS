# Primary-Replica Synchronization


class Database:
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.version = 0

    def update(self, key, value):
        self.data[key] = value
        self.version += 1

    def show(self):
        print(f"{self.name} data:", self.data)
        print(f"{self.name} version:", self.version)


class ReplicationManager:
    def __init__(self):
        self.primary = Database("Primary")
        self.replica = Database("Replica")

    def update_primary(self, key, value):
        self.primary.update(key, value)
        print("Primary updated")

    def synchronize(self):
        if self.primary.version != self.replica.version:
            self.replica.data = self.primary.data.copy()
            self.replica.version = self.primary.version
            print("Replica synchronized")
        else:
            print("Replica already synchronized")


manager = ReplicationManager()

manager.update_primary(1, "Alice")
manager.update_primary(2, "Bob")

manager.synchronize()

manager.primary.show()
manager.replica.show()
