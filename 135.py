# Database Transaction Lock Audit Logger


from datetime import datetime


class TransactionLockAuditLogger:
    def __init__(self):
        self.locks = {}
        self.audit_log = []

    def log_event(self, tx_id, resource, action, status):
        event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "transaction": tx_id,
            "resource": resource,
            "action": action,
            "status": status
        }

        self.audit_log.append(event)

    def request_lock(self, tx_id, resource):
        self.log_event(
            tx_id, resource, "LOCK_REQUEST", "RECEIVED"
        )

        if resource not in self.locks or self.locks[resource] == tx_id:
            self.locks[resource] = tx_id

            self.log_event(
                tx_id, resource, "LOCK_GRANTED", "SUCCESS"
            )
            return True

        owner = self.locks[resource]

        self.log_event(
            tx_id, resource, "LOCK_DENIED",
            f"BLOCKED_BY:{owner}"
        )
        return False

    def release_lock(self, tx_id, resource):
        self.log_event(
            tx_id, resource, "RELEASE_REQUEST", "RECEIVED"
        )

        if self.locks.get(resource) == tx_id:
            del self.locks[resource]

            self.log_event(
                tx_id, resource, "LOCK_RELEASED", "SUCCESS"
            )
            return True

        self.log_event(
            tx_id, resource, "RELEASE_REJECTED", "NOT_OWNER"
        )
        return False

    def show_audit_log(self):
        print("\nDATABASE LOCK AUDIT LOG")
        print("-" * 100)

        for event in self.audit_log:
            print(
                f"{event['timestamp']} | "
                f"{event['transaction']} | "
                f"{event['resource']} | "
                f"{event['action']} | "
                f"{event['status']}"
            )


logger = TransactionLockAuditLogger()

logger.request_lock("T1", "Account-A")
logger.request_lock("T2", "Account-A")
logger.release_lock("T1", "Account-A")
logger.request_lock("T2", "Account-A")
logger.release_lock("T2", "Account-A")

logger.show_audit_log()
