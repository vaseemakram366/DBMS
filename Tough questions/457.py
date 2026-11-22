# View Serializability Simulation


schedule = [
    ("T1", "Write", "A"),
    ("T2", "Write", "A"),
    ("T1", "Write", "A")
]

initial_writer = {}
final_writer = {}

for transaction, operation, data in schedule:
    if operation == "Write":
        if data not in initial_writer:
            initial_writer[data] = transaction

        final_writer[data] = transaction

print("Initial Writer:", initial_writer)
print("Final Writer:", final_writer)

serial_schedule = [
    ("T2", "Write", "A"),
    ("T1", "Write", "A")
]

serial_final_writer = {}

for transaction, operation, data in serial_schedule:
    if operation == "Write":
        serial_final_writer[data] = transaction

if final_writer == serial_final_writer:
    print("View Equivalent")
else:
    print("Not View Equivalent")
