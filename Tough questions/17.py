# Query Optimizer with Cost Estimation.

class QueryOptimizer:

    def __init__(self):
        self.plans = []

    def add_plan(self, name, operations):
        cost = 0

        for operation in operations:
            cost += operation["cost"]

        self.plans.append({
            "name": name,
            "operations": operations,
            "cost": cost
        })

    def optimize(self):
        if not self.plans:
            return None

        return min(
            self.plans,
            key=lambda plan: plan["cost"]
        )

    def display_plans(self):
        print("\nExecution Plans:")

        for plan in self.plans:
            print("\nPlan:", plan["name"])

            for operation in plan["operations"]:
                print(
                    " ",
                    operation["operation"],
                    "Cost:",
                    operation["cost"]
                )

            print("Total Cost:", plan["cost"])


optimizer = QueryOptimizer()

optimizer.add_plan(
    "Plan 1",
    [
        {
            "operation": "Table Scan Employees",
            "cost": 1000
        },
        {
            "operation": "Filter Department",
            "cost": 500
        },
        {
            "operation": "Join Departments",
            "cost": 800
        }
    ]
)

optimizer.add_plan(
    "Plan 2",
    [
        {
            "operation": "Index Scan Employees",
            "cost": 100
        },
        {
            "operation": "Filter Department",
            "cost": 50
        },
        {
            "operation": "Hash Join",
            "cost": 200
        }
    ]
)

optimizer.add_plan(
    "Plan 3",
    [
        {
            "operation": "Index Scan Employees",
            "cost": 100
        },
        {
            "operation": "Filter Department",
            "cost": 50
        },
        {
            "operation": "Nested Loop Join",
            "cost": 600
        }
    ]
)

optimizer.display_plans()

best = optimizer.optimize()

print("\n========== OPTIMIZED PLAN ==========")
print("Selected:", best["name"])
print("Minimum Cost:", best["cost"])