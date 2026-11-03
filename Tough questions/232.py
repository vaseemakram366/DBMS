# Conflict Serializability Checker


def is_conflict(a, b):
    t1, op1, item1 = a
    t2, op2, item2 = b

    return (
        t1 != t2
        and item1 == item2
        and (op1 == "WRITE" or op2 == "WRITE")
    )


def check_conflicts(schedule):
    print("Conflicting operation pairs:")

    found = False

    for i in range(len(schedule)):
        for j in range(i + 1, len(schedule)):
            if is_conflict(schedule[i], schedule[j]):
                print(schedule[i], "<->", schedule[j])
                found = True

    if not found:
        print("No conflicts found.")


schedule = [
    ("T1", "READ", "A"),
    ("T2", "WRITE", "A"),
    ("T1", "WRITE", "B"),
    ("T2", "READ", "B")
]

check_conflicts(schedule)
