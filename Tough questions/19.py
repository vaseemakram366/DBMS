# Sort-Merge Join
def sort_merge_join(table1, table2, key1, key2):
    table1 = sorted(table1, key=lambda row: row[key1])
    table2 = sorted(table2, key=lambda row: row[key2])

    i = 0
    j = 0
    result = []

    while i < len(table1) and j < len(table2):

        value1 = table1[i][key1]
        value2 = table2[j][key2]

        if value1 < value2:
            i += 1

        elif value1 > value2:
            j += 1

        else:
            start_j = j

            while (
                j < len(table2)
                and table2[j][key2] == value1
            ):
                j += 1

            for x in range(i, len(table1)):
                if table1[x][key1] != value1:
                    break

                for y in range(start_j, j):
                    result.append(
                        table1[x] + table2[y]
                    )

            while (
                i < len(table1)
                and table1[i][key1] == value1
            ):
                i += 1

    return result


employees = [
    (3, "Aman"),
    (1, "Vaseem"),
    (4, "Sara"),
    (2, "Rahul")
]

departments = [
    (2, "ECE"),
    (4, "AI"),
    (1, "CSE"),
    (3, "ME")
]

result = sort_merge_join(
    employees,
    departments,
    0,
    0
)

print("Sort-Merge Join Result:")

for row in result:
    print(row)