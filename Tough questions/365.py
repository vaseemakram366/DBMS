# Log Sequence Number (LSN) Simulation


class LogManager:
    def __init__(self):
        self.logs = []
        self.next_lsn = 1

    def add_log(self, tx, operation):
        record = {
            "LSN": self.next_lsn,
            "Transaction": tx,
            "Operation": operation
        }

        self.logs.append(record)

        print("Log added:", record)

        self.next_lsn += 1


manager = LogManager()

manager.add_log("T1", "BEGIN")
manager.add_log("T1", "UPDATE")
manager.add_log("T1", "COMMIT")
manager.add_log("T2", "BEGIN")
