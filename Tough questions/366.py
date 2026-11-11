# Recovery Using Before and After Images


database = {
    "balance": 1000
}

log = {
    "before_image": 1000,
    "after_image": 1500
}

def undo():
    database["balance"] = log["before_image"]
    print("UNDO completed!")
    print("Balance:", database["balance"])

def redo():
    database["balance"] = log["after_image"]
    print("REDO completed!")
    print("Balance:", database["balance"])


# Simulate an update
database["balance"] = log["after_image"]

print("After update:", database["balance"])

undo()
redo()
