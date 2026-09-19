# External Merge Sort — Disk-Based Sorting

import heapq
import os
import tempfile


class ExternalMergeSort:
    def __init__(self, memory_limit=5):
        self.memory_limit = memory_limit

    def create_sorted_runs(self, input_file, temp_dir):
        runs = []
        buffer = []

        with open(input_file, "r") as f:
            for line in f:
                buffer.append(int(line.strip()))

                if len(buffer) == self.memory_limit:
                    buffer.sort()

                    run_file = tempfile.NamedTemporaryFile(
                        mode="w",
                        delete=False,
                        dir=temp_dir
                    )

                    for num in buffer:
                        run_file.write(f"{num}\n")

                    run_file.close()
                    runs.append(run_file.name)
                    buffer.clear()

        if buffer:
            buffer.sort()

            run_file = tempfile.NamedTemporaryFile(
                mode="w",
                delete=False,
                dir=temp_dir
            )

            for num in buffer:
                run_file.write(f"{num}\n")

            run_file.close()
            runs.append(run_file.name)

        return runs

    def merge_runs(self, runs, output_file):
        files = [open(run, "r") for run in runs]
        heap = []

        for i, file in enumerate(files):
            value = file.readline()

            if value:
                heapq.heappush(heap, (int(value), i))

        with open(output_file, "w") as out:
            while heap:
                value, index = heapq.heappop(heap)
                out.write(f"{value}\n")

                next_value = files[index].readline()

                if next_value:
                    heapq.heappush(
                        heap,
                        (int(next_value), index)
                    )

        for file in files:
            file.close()

        for run in runs:
            os.remove(run)

    def sort(self, input_file, output_file):
        with tempfile.TemporaryDirectory() as temp_dir:
            runs = self.create_sorted_runs(
                input_file,
                temp_dir
            )

            self.merge_runs(
                runs,
                output_file
            )


def create_input_file(filename):
    data = [
        42, 17, 89, 3, 56,
        21, 8, 73, 14, 65,
        91, 2, 38, 50, 7
    ]

    with open(filename, "w") as f:
        for num in data:
            f.write(f"{num}\n")


input_file = "large_data.txt"
output_file = "sorted_data.txt"

create_input_file(input_file)

sorter = ExternalMergeSort(memory_limit=4)
sorter.sort(input_file, output_file)

with open(output_file, "r") as f:
    print("Sorted Data:")
    print([int(x.strip()) for x in f])