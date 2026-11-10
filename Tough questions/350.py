# Deadlock Recovery Using Victim Selection


def select_victim(transactions):
    victim = min(
        transactions,
        key=lambda tx: transactions[tx]
    )

    print("Deadlock detected!")
    print("Transaction costs:", transactions)
    print("Victim selected:", victim)
    print("Aborting transaction:", victim)
    print("Deadlock recovery completed.")


transactions = {
    "T1": 50,
    "T2": 20,
    "T3": 80
}

select_victim(transactions)
