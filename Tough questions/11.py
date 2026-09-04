# Hash Join Algorithm

def hash_join(table1, table2, key_index1, key_index2):

    hash_table = {}

    # Build phase
    for row in table1:

        key = row[key_index1]

        if key not in hash_table:
            hash_table[key] = []

        hash_table[key].append(row)

    result = []

    # Probe phase
    for row in table2:

        key = row[key_index2]

        if key in hash_table:

            for matching_row in hash_table[key]:

                result.append(
                    matching_row + row
                )

    return result


employees = [
    (1, "Vaseem"),
    (2, "Rahul"),
    (3, "Aman"),
    (4, "Sara")
]

departments = [
    (1, "CSE"),
    (2, "ECE"),
    (4, "AI")
]

result = hash_join(
    employees,
    departments,
    0,
    0
)

print("JOIN Result:")

for row in result:
    print(row)