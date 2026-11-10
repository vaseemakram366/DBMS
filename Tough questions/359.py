# Undo and Redo Operations


balance = 1000

def redo(amount):
    global balance
    balance += amount
    print("After REDO:", balance)

def undo(amount):
    global balance
    balance -= amount
    print("After UNDO:", balance)


print("Initial balance:", balance)

redo(500)
undo(500)
redo(500)
