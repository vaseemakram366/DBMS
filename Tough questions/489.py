# High Availability Database Simulation

servers = {
    "DB1": "ACTIVE",
    "DB2": "STANDBY",
    "DB3": "STANDBY"
}

print("Database Server Status:")

for server, status in servers.items():
    print(server, ":", status)

# Simulate DB1 failure
servers["DB1"] = "FAILED"
print("\nDB1 Failed")

# Activate another available server
for server in servers:
    if servers[server] == "STANDBY":
        servers[server] = "ACTIVE"
        print("Failover:", server, "Activated")
        break

print("\nFinal Server Status:")

for server, status in servers.items():
    print(server, ":", status)