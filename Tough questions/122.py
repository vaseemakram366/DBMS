# Database Transaction Throughput Benchmark

from concurrent.futures import ThreadPoolExecutor
from time import perf_counter, sleep
from math import ceil


class TransactionThroughputBenchmark:

    def __init__(self, transaction_count=40):
        self.transaction_count = transaction_count

    def execute_transaction(self, transaction_id):
        start = perf_counter()

        # Simulate database transaction processing
        sleep(0.02)

        latency = perf_counter() - start
        return latency

    def run(self, concurrency):
        start_time = perf_counter()

        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            latencies = list(
                executor.map(
                    self.execute_transaction,
                    range(self.transaction_count)
                )
            )

        total_time = perf_counter() - start_time

        tps = self.transaction_count / total_time
        avg_latency = sum(latencies) / len(latencies)

        sorted_latencies = sorted(latencies)
        p95_index = ceil(0.95 * len(sorted_latencies)) - 1
        p95_latency = sorted_latencies[p95_index]

        return {
            "concurrency": concurrency,
            "transactions": self.transaction_count,
            "time": total_time,
            "tps": tps,
            "avg_latency": avg_latency,
            "p95_latency": p95_latency
        }


benchmark = TransactionThroughputBenchmark(40)

print("DATABASE THROUGHPUT BENCHMARK")
print("-" * 70)

results = []

for workers in [1, 2, 4, 8]:
    result = benchmark.run(workers)
    results.append(result)

    print(f"\nConcurrency: {result['concurrency']}")
    print(f"Transactions: {result['transactions']}")
    print(f"Total Time: {result['time']:.3f} seconds")
    print(f"Throughput: {result['tps']:.2f} TPS")
    print(f"Average Latency: {result['avg_latency'] * 1000:.2f} ms")
    print(f"P95 Latency: {result['p95_latency'] * 1000:.2f} ms")

best = max(results, key=lambda item: item["tps"])

print("\n" + "-" * 70)
print(f"Best measured concurrency: {best['concurrency']} workers")
print(f"Best measured throughput: {best['tps']:.2f} TPS")