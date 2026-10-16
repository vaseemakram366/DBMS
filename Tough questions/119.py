# Database Transaction Timeout Manager


import multiprocessing
import time


def run_transaction(transaction, result_queue):
    try:
        result = transaction()
        result_queue.put(("SUCCESS", result))
    except Exception as error:
        result_queue.put(("ERROR", str(error)))


class TransactionTimeoutManager:
    def __init__(self, timeout_seconds=3):
        if timeout_seconds <= 0:
            raise ValueError("Timeout must be positive")

        self.timeout_seconds = timeout_seconds

    def execute(self, transaction):
        result_queue = multiprocessing.Queue()

        process = multiprocessing.Process(
            target=run_transaction,
            args=(transaction, result_queue)
        )

        print("Starting transaction...")
        start = time.monotonic()
        process.start()

        process.join(self.timeout_seconds)
        elapsed = time.monotonic() - start

        if process.is_alive():
            print("Transaction timeout detected!")
            process.terminate()
            process.join()
            result_queue.close()
            result_queue.join_thread()

            print("Transaction process terminated.")
            print("Elapsed time: {:.2f}s".format(elapsed))

            return {
                "status": "TIMEOUT",
                "result": None,
                "elapsed": elapsed
            }

        try:
            status, result = result_queue.get(timeout=1)
        except Exception:
            status, result = "ERROR", "No result received"
        finally:
            result_queue.close()
            result_queue.join_thread()

        print("Transaction status:", status)
        print("Elapsed time: {:.2f}s".format(elapsed))

        return {
            "status": status,
            "result": result,
            "elapsed": elapsed
        }


def successful_transaction():
    time.sleep(1)
    return "Account updated successfully"


def slow_transaction():
    time.sleep(5)
    return "This should time out"


if __name__ == "__main__":
    manager = TransactionTimeoutManager(timeout_seconds=2)

    print("\n--- Test 1: Successful transaction ---")
    print(manager.execute(successful_transaction))

    print("\n--- Test 2: Slow transaction ---")
    print(manager.execute(slow_transaction))
