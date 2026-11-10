# Cascading Rollback


def cascading_rollback(dependencies, failed_tx):
    rollback = set()

    def find_dependents(tx):
        if tx in rollback:
            return

        rollback.add(tx)

        for dependent in dependencies.get(tx, []):
            find_dependents(dependent)

    find_dependents(failed_tx)

    print("Failed transaction:", failed_tx)
    print("Transactions to rollback:")

    for tx in sorted(rollback):
        print(tx)


dependencies = {
    "T1": ["T2"],
    "T2": ["T3"],
    "T3": [],
    "T4": []
}

cascading_rollback(dependencies, "T1")
