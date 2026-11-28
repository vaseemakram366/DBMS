# Database Load Balancing Simulation

servers = {
    "DB1": 0,
    "DB2": 0,
    "DB3": 0
}

requests = 9

for i in range(requests):
    # Select server with minimum load
    selected_server = min(servers, key=servers.get)

    # Assign request
    servers[selected_server] += 1

    print(f"Request {i + 1} -> {selected_server}")

print("\nFinal Server Loads:")

for server, load in servers.items():
    print(server, ":", load)