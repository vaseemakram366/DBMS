# Distributed Sorting


import heapq

class DistributedSorting:
    def __init__(self):
        self.shards = {
            "Server A": [8, 3, 5],
            "Server B": [4, 9, 1],
            "Server C": [7, 2, 6]
        }

    def sort_data(self):
        sorted_parts = []

        for server, values in self.shards.items():
            local_sorted = sorted(values)
            sorted_parts.append(local_sorted)

            print(f"{server} sorted data: {local_sorted}")

        final_result = list(heapq.merge(*sorted_parts))

        print("Final sorted data:", final_result)


db = DistributedSorting()
db.sort_data()
