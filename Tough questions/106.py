# Database Top-K Query Engine


import heapq


class TopKQueryEngine:
    def __init__(self, k):
        if k <= 0:
            raise ValueError("K must be positive")

        self.k = k

    def top_k(self, records, field):
        heap = []

        for record in records:
            if field not in record:
                raise ValueError(f"Missing field: {field}")

            value = record[field]
            item = (value, record["id"], record)

            if len(heap) < self.k:
                heapq.heappush(heap, item)
            elif value > heap[0][0]:
                heapq.heapreplace(heap, item)

        return [
            item[2]
            for item in sorted(heap, reverse=True)
        ]


employees = [
    {"id": 1, "name": "Aman", "salary": 30000},
    {"id": 2, "name": "Riya", "salary": 60000},
    {"id": 3, "name": "Rahul", "salary": 45000},
    {"id": 4, "name": "Neha", "salary": 80000},
    {"id": 5, "name": "Karan", "salary": 55000},
    {"id": 6, "name": "Priya", "salary": 75000},
    {"id": 7, "name": "Arjun", "salary": 40000}
]

engine = TopKQueryEngine(k=3)

result = engine.top_k(employees, "salary")

print("Top 3 highest-paid employees:")
for employee in result:
    print(employee)
