# Write-Ahead Logging (WAL) Simulation


database = {
    "balance": 1000
}

log = []

def update_balance(amount):
    old_value = database["balance"]
    new_value = old_value + amount

    # Step 1: Write log first
    log_record = {
        "old": old_value,
        "new": new_value
    }

    log.append(log_record)
    print("Log written:", log_record)

    # Step 2: Update database
    database["balance"] = new_value
    print("Database updated:", database["balance"])


print("Initial balance:", database["balance"])

update_balance(500)

print("Final balance:", database["balance"])
