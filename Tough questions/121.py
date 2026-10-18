# Database Connection Pool Load Balancer


import threading
import time
from concurrent.futures import ThreadPoolExecutor


class DatabaseConnection:
    def __init__(self, connection_id):
        self.connection_id = connection_id
        self.active_requests = 0
        self.total_requests = 0


class ConnectionPoolLoadBalancer:
    def __init__(self, pool_size=3):
        if pool_size <= 0:
            raise ValueError("Pool size must be positive")

        self.connections = [
            DatabaseConnection(i + 1)
            for i in range(pool_size)
        ]
        self.condition = threading.Condition()

    def acquire(self, timeout=5):
        deadline = time.monotonic() + timeout

        with self.condition:
            while True:
                available = [
                    conn for conn in self.connections
                    if conn.active_requests == 0
                ]

                if available:
                    conn = min(
                        available,
                        key=lambda item: item.total_requests
                    )
                    conn.active_requests += 1
                    conn.total_requests += 1
                    return conn

                remaining = deadline - time.monotonic()

                if remaining <= 0:
                    raise TimeoutError("No connection available")

                self.condition.wait(remaining)

    def release(self, connection):
        with self.condition:
            if connection.active_requests <= 0:
                raise ValueError("Connection is not checked out")

            connection.active_requests -= 1
            self.condition.notify()

    def execute_request(self, request_id, work_seconds=1):
        connection = self.acquire()

        try:
            print(
                f"Request {request_id} assigned to "
                f"Connection {connection.connection_id}"
            )
            time.sleep(work_seconds)
            return f"Request {request_id} completed"
        finally:
            self.release(connection)

    def report(self):
        print("\n===== Connection Pool Report =====")

        for conn in self.connections:
            print(
                f"Connection {conn.connection_id}: "
                f"active={conn.active_requests}, "
                f"total requests={conn.total_requests}"
            )


if __name__ == "__main__":
    pool = ConnectionPoolLoadBalancer(pool_size=3)

    with ThreadPoolExecutor(max_workers=6) as executor:
        futures = [
            executor.submit(pool.execute_request, i, 0.5)
            for i in range(1, 7)
        ]

        for future in futures:
            print(future.result())

    pool.report()
