# Checkpoint Recovery Simulation


database = {"balance": 5000}

log = [
    {"type": "UPDATE", "balance": 6000},
    {"type": "CHECKPOINT", "balance": 6000},
    {"type": "UPDATE", "balance": 8000},
    {"type": "UPDATE", "balance": 9000}
]

print("Database Before Recovery:", 5000)

checkpoint = None

for record in log:
    if record["type"] == "CHECKPOINT":
        checkpoint = record

if checkpoint:
    database["balance"] = checkpoint["balance"]

    for record in log[log.index(checkpoint) + 1:]:
        if record["type"] == "UPDATE":
            database["balance"] = record["balance"]

print("Checkpoint Found")
print("Database After Recovery:", database["balance"])
