# Distributed Transaction Coordinator


class TransactionCoordinator:
    def __init__(self):
        self.servers = ["Server A", "Server B", "Server C"]
        self.transaction_log = []

    def execute_transaction(self, transaction_id):
        print("Transaction ID:", transaction_id)

        print("\nPreparing servers:")

        for server in self.servers:
            print(server, "is ready")
            self.transaction_log.append(
                (server, "PREPARED")
            )

        print("\nCommitting transaction:")

        for server in self.servers:
            print(server, "COMMITTED")
            self.transaction_log.append(
                (server, "COMMITTED")
            )

        print("\nTransaction completed successfully")

        print("\nTransaction Log:")
        for entry in self.transaction_log:
            print(entry)


coordinator = TransactionCoordinator()
coordinator.execute_transaction("TXN101")
