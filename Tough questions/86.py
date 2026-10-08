# Adaptive Query Execution / Runtime Re-Optimization

class QueryPlan:
    def __init__(self, name, estimated_rows, cost):
        self.name = name
        self.estimated_rows = estimated_rows
        self.cost = cost

    def __str__(self):
        return (
            f"{self.name} "
            f"(estimated rows={self.estimated_rows}, "
            f"cost={self.cost})"
        )


class AdaptiveQueryExecutor:
    def __init__(self):
        self.reoptimized = False

    def choose_plan(self, estimated_rows):
        if estimated_rows < 1000:
            return QueryPlan(
                "Nested Loop Join",
                estimated_rows,
                estimated_rows * 2
            )

        return QueryPlan(
            "Hash Join",
            estimated_rows,
            estimated_rows
        )

    def execute(self, plan, actual_rows):
        print("Initial plan:")
        print(plan)

        error_ratio = actual_rows / max(
            plan.estimated_rows, 1
        )

        print("Actual rows:", actual_rows)

        if error_ratio > 10 or error_ratio < 0.1:
            print("Large cardinality mismatch detected")
            print("Re-optimizing query...")

            new_plan = self.choose_plan(actual_rows)

            self.reoptimized = True

            print("New plan:")
            print(new_plan)

            return new_plan

        print("Original plan retained")
        return plan


executor = AdaptiveQueryExecutor()

initial_plan = executor.choose_plan(500)

final_plan = executor.execute(
    initial_plan,
    actual_rows=50000
)

print("\nFinal plan:")
print(final_plan)