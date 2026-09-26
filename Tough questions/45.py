# Database Replication Manager

from copy import deepcopy


class DatabaseNode:
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.log = []
        self.alive = True
        self.last_lsn = 0

    def apply_operation(self, operation):
        if not self.alive:
            return False

        lsn = operation["lsn"]
        op = operation["operation"]
        key = operation["key"]
        value = operation["value"]

        if lsn <= self.last_lsn:
            return True

        if op == "SET":
            self.data[key] = value

        elif op == "DELETE":
            self.data.pop(key, None)

        self.log.append(deepcopy(operation))
        self.last_lsn = lsn

        return True

    def show(self):
        print(
            f"{self.name}: "
            f"LSN={self.last_lsn}, "
            f"Data={self.data}"
        )


class ReplicationManager:
    def __init__(self):
        self.primary = None
        self.replicas = []
        self.next_lsn = 1

    def add_primary(self, node):
        self.primary = node
        print(f"Primary: {node.name}")

    def add_replica(self, node):
        self.replicas.append(node)

        if self.primary:
            for operation in self.primary.log:
                node.apply_operation(operation)

        print(f"Replica added: {node.name}")

    def write(self, key, value):
        if self.primary is None:
            print("No primary available")
            return

        if not self.primary.alive:
            print("Primary is down")
            return

        operation = {
            "lsn": self.next_lsn,
            "operation": "SET",
            "key": key,
            "value": value
        }

        self.next_lsn += 1

        self.primary.apply_operation(operation)

        for replica in self.replicas:
            if replica.alive:
                replica.apply_operation(operation)

        print(
            f"WRITE {key}={value} "
            f"LSN={operation['lsn']}"
        )

    def delete(self, key):
        if self.primary is None:
            return

        operation = {
            "lsn": self.next_lsn,
            "operation": "DELETE",
            "key": key,
            "value": None
        }

        self.next_lsn += 1

        self.primary.apply_operation(operation)

        for replica in self.replicas:
            if replica.alive:
                replica.apply_operation(operation)

    def fail_node(self, node):
        node.alive = False
        print(f"{node.name} FAILED")

    def recover_node(self, node):
        node.alive = True

        if self.primary:
            for operation in self.primary.log:
                node.apply_operation(operation)

        print(f"{node.name} RECOVERED")

    def promote(self, replica):
        if replica not in self.replicas:
            return

        if not replica.alive:
            print("Cannot promote failed replica")
            return

        old_primary = self.primary

        self.primary = replica

        self.replicas.remove(replica)

        if old_primary:
            self.replicas.append(old_primary)

        print(
            f"{replica.name} promoted to PRIMARY"
        )

    def show_cluster(self):
        print("\nCluster State:")

        if self.primary:
            self.primary.show()

        for replica in self.replicas:
            replica.show()


primary = DatabaseNode("DB-Primary")
replica1 = DatabaseNode("DB-Replica-1")
replica2 = DatabaseNode("DB-Replica-2")

manager = ReplicationManager()

manager.add_primary(primary)
manager.add_replica(replica1)
manager.add_replica(replica2)

manager.write("A", 100)
manager.write("B", 200)
manager.write("C", 300)

manager.show_cluster()

print("\nPrimary failure:")

manager.fail_node(primary)

manager.promote(replica1)

manager.write("D", 400)

manager.show_cluster()

print("\nRecovering old primary:")

manager.recover_node(primary)

manager.show_cluster()