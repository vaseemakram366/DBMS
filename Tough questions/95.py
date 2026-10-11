# Temporal Database Engine


from datetime import datetime


class TemporalDatabase:
    def __init__(self):
        self.records = {}

    def insert(self, record_id, data):
        if record_id in self.records:
            raise ValueError("Record already exists")

        now = datetime.now()

        self.records[record_id] = [{
            "data": data.copy(),
            "valid_from": now,
            "valid_to": None
        }]

    def update(self, record_id, new_data):
        if record_id not in self.records:
            raise ValueError("Record not found")

        history = self.records[record_id]
        current = history[-1]

        if current["valid_to"] is not None:
            raise ValueError("No active version found")

        now = datetime.now()
        current["valid_to"] = now

        history.append({
            "data": new_data.copy(),
            "valid_from": now,
            "valid_to": None
        })

    def get_current(self, record_id):
        history = self.records.get(record_id, [])

        for version in reversed(history):
            if version["valid_to"] is None:
                return version["data"].copy()

        return None

    def get_history(self, record_id):
        return self.records.get(record_id, [])

    def get_at(self, record_id, timestamp):
        history = self.records.get(record_id, [])

        for version in history:
            start = version["valid_from"]
            end = version["valid_to"]

            if start <= timestamp and (end is None or timestamp < end):
                return version["data"].copy()

        return None


db = TemporalDatabase()

db.insert(101, {"name": "Aman", "salary": 30000})

old_version = db.get_history(101)[0]
old_time = old_version["valid_from"]

db.update(101, {"name": "Aman", "salary": 45000})

print("Current record:", db.get_current(101))
print("Record at old time:", db.get_at(101, old_time))

print("\nComplete history:")
for version in db.get_history(101):
    print(version)
