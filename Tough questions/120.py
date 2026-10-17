# Database Connection Leak Detector


import time


class ConnectionLeakDetector:
    def __init__(self, leak_threshold_seconds=5):
        if leak_threshold_seconds < 0:
            raise ValueError("Threshold cannot be negative")

        self.leak_threshold = leak_threshold_seconds
        self.connections = {}
        self.next_id = 1

    def acquire(self, owner):
        connection_id = self.next_id
        self.next_id += 1

        self.connections[connection_id] = {
            "owner": owner,
            "created_at": time.monotonic(),
            "released": False
        }

        print(f"Connection {connection_id} acquired by {owner}")
        return connection_id

    def release(self, connection_id):
        connection = self.connections.get(connection_id)

        if connection is None:
            raise ValueError("Unknown connection ID")

        if connection["released"]:
            raise ValueError("Connection already released")

        connection["released"] = True
        print(f"Connection {connection_id} released")

    def analyze(self):
        now = time.monotonic()
        findings = []

        for connection_id, connection in self.connections.items():
            if connection["released"]:
                continue

            age = now - connection["created_at"]

            if age >= self.leak_threshold:
                findings.append({
                    "connection_id": connection_id,
                    "owner": connection["owner"],
                    "age_seconds": age,
                    "status": "POTENTIAL LEAK"
                })

        return findings

    def report(self):
        active = [
            connection
            for connection in self.connections.values()
            if not connection["released"]
        ]

        findings = self.analyze()

        print("\n===== Connection Leak Report =====")
        print(f"Total connections: {len(self.connections)}")
        print(f"Active connections: {len(active)}")
        print(f"Released connections: "
              f"{len(self.connections) - len(active)}")
        print(f"Potential leaks: {len(findings)}")

        for item in findings:
            print(f"\nConnection ID: {item['connection_id']}")
            print(f"Owner: {item['owner']}")
            print(f"Open for: {item['age_seconds']:.2f} seconds")
            print(f"Status: {item['status']}")


detector = ConnectionLeakDetector(leak_threshold_seconds=2)

conn1 = detector.acquire("UserService")
conn2 = detector.acquire("OrderService")

detector.release(conn1)

time.sleep(2.2)

detector.report()
