# Database Recovery Simulation


database = {"balance": 5000}

log = [
    {"old": 5000, "new": 6000, "committed": True},
    {"old": 6000, "new": 8000, "committed": False}
]

print("Database Before Recovery:", database["balance"])

# Simulate system crash
database["balance"] = 6000

print("System Crash Occurred")

# Recovery process
for record in log:
    if record["committed"]:
        database["balance"] = record["new"]
    else:
        database["balance"] = record["old"]

print("Database After Recovery:", database["balance"])
