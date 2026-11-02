# Query Optimizer Using Join Costs


def estimate_cost(n, m):
    costs = {
        "Nested Loop Join": n * m,
        "Hash Join": n + m,
        "Sort-Merge Join": (
            n * (n.bit_length()) +
            m * (m.bit_length())
        )
    }

    return costs


def optimize_query(n, m):
    costs = estimate_cost(n, m)

    print("Estimated query costs:")
    for plan, cost in costs.items():
        print(f"{plan}: {cost}")

    best_plan = min(costs, key=costs.get)

    print("Selected plan:", best_plan)


optimize_query(100, 200)
