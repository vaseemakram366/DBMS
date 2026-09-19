# Database Join — Block Nested Loop Join

class BlockNestedLoopJoin:

    def __init__(self, block_size):
        self.block_size = block_size

    def join(self, outer_table, inner_table, outer_key, inner_key):
        result = []

        for start in range(0, len(outer_table), self.block_size):

            block = outer_table[
                start:start + self.block_size
            ]

            print(
                "\nProcessing outer block:",
                block
            )

            for outer_row in block:

                for inner_row in inner_table:

                    if (
                        outer_row[outer_key]
                        == inner_row[inner_key]
                    ):
                        result.append(
                            outer_row + inner_row
                        )

        return result


employees = [
    (1, "Vaseem"),
    (2, "Rahul"),
    (3, "Aman"),
    (4, "Sara"),
    (5, "Karan")
]

departments = [
    (1, "CSE"),
    (2, "ECE"),
    (3, "AI"),
    (4, "ME"),
    (5, "IT")
]

joiner = BlockNestedLoopJoin(
    block_size=2
)

result = joiner.join(
    employees,
    departments,
    0,
    0
)

print("\nJOIN RESULT:")

for row in result:
    print(row)