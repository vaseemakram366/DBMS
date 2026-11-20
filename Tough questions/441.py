# Concurrency Control Simulation


import threading

account = {"balance": 5000}
lock = threading.Lock()

def deposit(amount):
    with lock:
        account["balance"] += amount
        print("Deposited:", amount)

def withdraw(amount):
    with lock:
        if account["balance"] >= amount:
            account["balance"] -= amount
            print("Withdrawn:", amount)
        else:
            print("Insufficient Balance")

t1 = threading.Thread(target=deposit, args=(1000,))
t2 = threading.Thread(target=withdraw, args=(2000,))

t1.start()
t2.start()

t1.join()
t2.join()

print("Final Balance:", account["balance"])
