# Transaction Scheduler Simulator


schedule = [
    ("T1", "READ", "A"),
    ("T2", "READ", "B"),
    ("T1", "WRITE", "A"),
    ("T2", "WRITE", "B"),
    ("T1", "READ", "B"),
    ("T2", "READ", "A")
]


def run_scheduler(schedule):
    print("Transaction Schedule:")

    for step, (transaction, operation, item) in enumerate(
        schedule, start=1
    ):
        print(
            f"Step {step}: {transaction} "
            f"{operation}({item})"
        )


run_scheduler(schedule)
