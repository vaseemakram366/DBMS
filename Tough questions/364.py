# Database Transaction Log Manager


class LogManager:
    def __init__(self):
        self.logs = []

    def write_log(self, tx, operation):
        self.logs.append((tx, operation))
        print(f"Log added: {tx} - {operation}")

    def display_logs(self):
        print("\nTransaction Logs:")

        for log in self.logs:
            print(log)


manager = LogManager()

manager.write_log("T1", "BEGIN")
manager.write_log("T1", "UPDATE")
manager.write_log("T1", "COMMIT")

manager.write_log("T2", "BEGIN")
manager.write_log("T2", "ABORT")

manager.display_logs()
