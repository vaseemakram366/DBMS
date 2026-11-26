# Recovery Manager Simulation

database = {"balance": 5000}

log = [
    {"old": 5000, "new": 7000, "committed": True},
    {"old": 7000, "new": 9000, "committed": False}
]

# Simulate updates before crash
database["balance"] = 9000

print("Before Recovery:", database["balance"])

# Recovery Manager
for record in reversed(log):
    if not record["committed"]:
        database["balance"] = record["old"]

for record in log:
    if record["committed"]:
        database["balance"] = record["new"]

print("Recovery Manager Activated")
print("After Recovery:", database["balance"])