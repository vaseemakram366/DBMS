# Phantom Read Simulation


employees = [
    {"id": 1, "name": "Alice", "salary": 30000},
    {"id": 2, "name": "Bob", "salary": 40000}
]

print("Transaction 1 - First Read:")

result1 = [
    emp for emp in employees
    if emp["salary"] > 25000
]

for emp in result1:
    print(emp)

employees.append({
    "id": 3,
    "name": "Charlie",
    "salary": 35000
})

print("\nTransaction 2 - New Employee Inserted")

print("\nTransaction 1 - Second Read:")

result2 = [
    emp for emp in employees
    if emp["salary"] > 25000
]

for emp in result2:
    print(emp)
