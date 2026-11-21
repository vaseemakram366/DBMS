# Deadlock Prevention Simulation


resources = ["Resource A", "Resource B"]

def transaction(name):
    print(name, "started")

    for resource in resources:
        print(name, "acquired", resource)

    print(name, "completed")

transaction("Transaction 1")
print()
transaction("Transaction 2")
