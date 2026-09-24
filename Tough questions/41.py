# Cost-Based Join Order Optimizer

from functools import lru_cache


class JoinOrderOptimizer:
    def __init__(self, tables, join_costs):
        self.tables = tables
        self.join_costs = join_costs

    def cost(self, left, right):
        key1 = (left, right)
        key2 = (right, left)

        if key1 in self.join_costs:
            return self.join_costs[key1]

        return self.join_costs[key2]

    def optimize(self):
        n = len(self.tables)

        @lru_cache(None)
        def dp(mask):
            if mask & (mask - 1) == 0:
                index = mask.bit_length() - 1
                table = self.tables[index]

                return 0, table

            best_cost = float("inf")
            best_plan = None

            submask = (mask - 1) & mask

            while submask:
                other = mask ^ submask

                if other != 0:
                    left_cost, left_plan = dp(submask)
                    right_cost, right_plan = dp(other)

                    left_tables = self.get_tables(submask)
                    right_tables = self.get_tables(other)

                    join = 0

                    for left in left_tables:
                        for right in right_tables:
                            join += self.cost(left, right)

                    total_cost = (
                        left_cost +
                        right_cost +
                        join
                    )

                    if total_cost < best_cost:
                        best_cost = total_cost

                        best_plan = (
                            f"({left_plan} JOIN "
                            f"{right_plan})"
                        )

                submask = (submask - 1) & mask

            return best_cost, best_plan

        full_mask = (1 << n) - 1

        return dp(full_mask)

    def get_tables(self, mask):
        result = []

        for i, table in enumerate(self.tables):
            if mask & (1 << i):
                result.append(table)

        return result


tables = [
    "Employees",
    "Departments",
    "Projects",
    "Locations"
]

join_costs = {
    ("Employees", "Departments"): 10,
    ("Employees", "Projects"): 50,
    ("Employees", "Locations"): 80,
    ("Departments", "Projects"): 15,
    ("Departments", "Locations"): 20,
    ("Projects", "Locations"): 60
}

optimizer = JoinOrderOptimizer(
    tables,
    join_costs
)

cost, plan = optimizer.optimize()

print("Optimal Join Plan:")
print(plan)

print("\nEstimated Cost:")
print(cost)