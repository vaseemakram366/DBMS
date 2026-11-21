# Pessimistic Concurrency Control Simulation


import threading

database = {"balance": 5000}
lock = threading.Lock()

def transaction(name, amount):
    with lock:
        print(name, "acquired lock")

        database["balance"] += amount

        print(name, "updated balance:", database["balance"])
        print(name, "released lock")


t1 = threading.Thread(target=transaction, args=("T1", 1000))
t2 = threading.Thread(target=transaction, args=("T2", 2000))

t1.start()
t2.start()

t1.join()
t2.join()

print("Final Balance:", database["balance"])
