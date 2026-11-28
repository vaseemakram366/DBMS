# Write Scaling Simulation

shards = {
    "DB1": {},
    "DB2": {},
    "DB3": {}
}

records = {
    101: "Aman",
    102: "Rahul",
    103: "Priya",
    104: "Karan",
    105: "Rohit",
    106: "Neha"
}

for student_id, name in records.items():
    # Select shard using modulo
    shard_number = student_id % 3
    server = f"DB{shard_number + 1}"

    # Write record into selected shard
    shards[server][student_id] = name

    print(f"Record {student_id} -> {server}")

print("\nFinal Shard Data:")

for server, data in shards.items():
    print(server, ":", data)