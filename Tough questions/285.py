# Multi-Version Concurrency Control (MVCC)


class MVCC:
    def __init__(self):
        self.data = {
            "balance": [
                {"version": 1, "value": 1000}
            ]
        }

    def write(self, value):
        new_version = len(self.data["balance"]) + 1

        self.data["balance"].append({
            "version": new_version,
            "value": value
        })

        print("New version created:", new_version)

    def read(self, version):
        for record in self.data["balance"]:
            if record["version"] == version:
                print("Read version:", version)
                print("Balance:", record["value"])
                return

        print("Version not found")

    def display_versions(self):
        print("\nAll Versions:")
        for record in self.data["balance"]:
            print(record)


db = MVCC()

db.write(1500)
db.write(2000)

db.read(1)
db.read(2)
db.read(3)

db.display_versions()
