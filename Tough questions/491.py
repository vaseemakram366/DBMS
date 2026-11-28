# Read Scaling Simulation

primary_db = {
    "101": "Aman",
    "102": "Rahul",
    "103": "Priya"
}

replicas = [
    primary_db.copy(),
    primary_db.copy(),
    primary_db.copy()
]

read_requests = ["101", "102", "103", "101", "102", "103"]

server_load = [0, 0, 0]

for i, key in enumerate(read_requests):
    # Round Robin server selection
    server_index = i % len(replicas)

    result = replicas[server_index][key]
    server_load[server_index] += 1

    print(f"Read {key} from Replica {server_index + 1}: {result}")

print("\nReplica Loads:")

for i, load in enumerate(server_load):
    print(f"Replica {i + 1}: {load}")