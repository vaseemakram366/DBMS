# Timestamp-Based Concurrency Control


transactions = {
    "T1": 1,
    "T2": 2
}

data = {
    "value": 100,
    "read_timestamp": 0,
    "write_timestamp": 0
}

def read(transaction):
    timestamp = transactions[transaction]

    if timestamp < data["write_timestamp"]:
        print(transaction, "Read Rejected")
    else:
        data["read_timestamp"] = max(
            data["read_timestamp"], timestamp
        )
        print(transaction, "Read Successful:", data["value"])

def write(transaction, value):
    timestamp = transactions[transaction]

    if timestamp < data["read_timestamp"] or timestamp < data["write_timestamp"]:
        print(transaction, "Write Rejected")
    else:
        data["value"] = value
        data["write_timestamp"] = timestamp
        print(transaction, "Write Successful:", value)


read("T1")
write("T2", 200)
read("T1")

print("Final Value:", data["value"])
