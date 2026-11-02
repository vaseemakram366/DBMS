# Query Cost Estimator


import math


class QueryCostEstimator:
    def __init__(self, total_rows, selectivity):
        self.total_rows = total_rows
        self.selectivity = selectivity

    def estimate(self):
        matching_rows = math.ceil(
            self.total_rows * self.selectivity
        )

        table_scan_cost = self.total_rows

        index_scan_cost = (
            math.ceil(math.log2(self.total_rows))
            + matching_rows
        )

        print("Total rows:", self.total_rows)
        print("Estimated matching rows:", matching_rows)
        print("Table scan cost:", table_scan_cost)
        print("Index scan cost:", index_scan_cost)

        if index_scan_cost < table_scan_cost:
            print("Chosen plan: INDEX SCAN")
        else:
            print("Chosen plan: TABLE SCAN")


estimator = QueryCostEstimator(
    total_rows=1000,
    selectivity=0.02
)

estimator.estimate()
