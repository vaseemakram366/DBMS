# DISTINCT with Multiple Columns


employees = [
    {"name": "Alice", "department": "CSE", "city": "Delhi"},
    {"name": "Bob", "department": "IT", "city": "Mumbai"},
    {"name": "Charlie", "department": "CSE", "city": "Delhi"},
    {"name": "David", "department": "CSE", "city": "Pune"},
    {"name": "Emma", "department": "IT", "city": "Mumbai"}
]

unique_combinations = set()

print("DISTINCT Result:")

for employee in employees:
    combination = (
        employee["department"],
        employee["city"]
    )

    if combination not in unique_combinations:
        unique_combinations.add(combination)
        print(combination)
