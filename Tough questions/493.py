# Database Sharding Simulation

shards = {
    "Shard1": {},
    "Shard2": {},
    "Shard3": {}
}

students = {
    101: "Aman",
    102: "Rahul",
    103: "Priya",
    104: "Karan",
    105: "Rohit",
    106: "Neha"
}

# Distribute records into shards
for student_id, name in students.items():
    shard_number = student_id % 3
    shard_name = f"Shard{shard_number + 1}"

    shards[shard_name][student_id] = name

print("Database Sharding Result:")

for shard, data in shards.items():
    print(shard, ":", data)