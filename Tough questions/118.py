# feat: implement database query plan regression detector


import random
import time


class RetryableDatabaseError(Exception):
    pass


class NonRetryableDatabaseError(Exception):
    pass


class TransactionRetryManager:
    def __init__(
        self,
        max_attempts=4,
        base_delay=0.1,
        max_delay=2.0,
        jitter=True
    ):
        if max_attempts < 1:
            raise ValueError("max_attempts must be at least 1")
        if base_delay < 0 or max_delay < 0:
            raise ValueError("Delays cannot be negative")

        self.max_attempts = max_attempts
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter

    def execute(self, transaction):
        for attempt in range(1, self.max_attempts + 1):
            try:
                print(f"Transaction attempt {attempt}")
                result = transaction()
                print("Transaction completed successfully")
                return result

            except RetryableDatabaseError as error:
                print(f"Retryable error: {error}")

                if attempt == self.max_attempts:
                    print("Maximum attempts reached")
                    raise

                delay = min(
                    self.base_delay * (2 ** (attempt - 1)),
                    self.max_delay
                )

                if self.jitter:
                    delay = random.uniform(0, delay)

                print(f"Retrying after {delay:.3f} seconds")
                time.sleep(delay)

            except NonRetryableDatabaseError:
                print("Non-retryable error; aborting transaction")
                raise


# Simulated transaction for demonstration
attempt_count = 0


def sample_transaction():
    global attempt_count
    attempt_count += 1

    if attempt_count < 3:
        raise RetryableDatabaseError("Simulated deadlock")

    return "Account updated"


manager = TransactionRetryManager(
    max_attempts=4,
    base_delay=0.1,
    max_delay=1.0,
    jitter=False
)

result = manager.execute(sample_transaction)
print("Result:", result)
    