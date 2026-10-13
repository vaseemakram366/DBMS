# Database Connection Pool Manager


from queue import Queue, Empty
from threading import Lock


class DatabaseConnection:
    def __init__(self, connection_id):
        self.connection_id = connection_id
        self.is_closed = False

    def execute(self, query):
        if self.is_closed:
            raise RuntimeError("Connection is closed")

        print(
            f"Connection {self.connection_id} "
            f"executing: {query}"
        )

    def close(self):
        self.is_closed = True


class ConnectionPool:
    def __init__(self, pool_size):
        if pool_size <= 0:
            raise ValueError("Pool size must be positive")

        self.pool = Queue(maxsize=pool_size)
        self.lock = Lock()
        self.available = 0

        for i in range(1, pool_size + 1):
            self.pool.put(DatabaseConnection(i))
            self.available += 1

    def acquire(self, timeout=2):
        try:
            connection = self.pool.get(timeout=timeout)

            with self.lock:
                self.available -= 1

            print(f"Acquired connection {connection.connection_id}")
            return connection

        except Empty:
            raise TimeoutError("No connection available")

    def release(self, connection):
        if connection.is_closed:
            raise ValueError("Cannot release a closed connection")

        self.pool.put(connection)

        with self.lock:
            self.available += 1

        print(f"Released connection {connection.connection_id}")

    def status(self):
        with self.lock:
            print(
                f"Available connections: {self.available}"
            )


pool = ConnectionPool(pool_size=2)

pool.status()

conn1 = pool.acquire()
conn2 = pool.acquire()

conn1.execute("SELECT * FROM students")
conn2.execute("SELECT * FROM employees")

pool.status()

pool.release(conn1)
pool.release(conn2)

pool.status()

conn3 = pool.acquire()
conn3.execute("SELECT * FROM courses")
pool.release(conn3)
