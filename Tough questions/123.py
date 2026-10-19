# Transaction Contention Analyzer


from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from time import perf_counter, sleep
from statistics import mean


class TransactionContentionAnalyzer:

    def __init__(self, transaction_count=20):
        self.transaction_count = transaction_count
        self.resource_lock = Lock()

    def execute_transaction(self, transaction_id):
        wait_start = perf_counter()

        with self.resource_lock:
            wait_time = perf_counter() - wait_start

            # Simulate work while holding the resource lock
            sleep(0.01)

        return wait_time

    def analyze(self, concurrency):
        start_time = perf_counter()

        with ThreadPoolExecutor(max_workers=concurrency) as executor:
            wait_times = list(
                executor.map(
                    self.execute_transaction,
                    range(self.transaction_count)
                )
            )

        total_time = perf_counter() - start_time
        total_wait = sum(wait_times)
        average_wait = mean(wait_times)

        contended = sum(
            1 for wait in wait_times if wait > 0.001
        )

        return {
            "concurrency": concurrency,
            "total_time": total_time,
            "total_wait": total_wait,
            "average_wait": average_wait,
            "contended": contended,
            "transactions": self.transaction_count
        }


analyzer = TransactionContentionAnalyzer(20)

print("TRANSACTION CONTENTION ANALYZER")
print("-" * 55)

for workers in [1, 2, 4, 8]:
    result = analyzer.analyze(workers)

    print(f"\nConcurrency: {result['concurrency']}")
    print(f"Transactions: {result['transactions']}")
    print(f"Total Execution Time: {result['total_time']:.3f} sec")
    print(f"Total Accumulated Wait: {result['total_wait']:.3f} sec")
    print(
        f"Average Wait: "
        f"{result['average_wait'] * 1000:.2f} ms"
    )
    print(
        f"Contended Transactions: "
        f"{result['contended']}/{result['transactions']}"
    )
