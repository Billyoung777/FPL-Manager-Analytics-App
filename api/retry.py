
import time
import requests


def retry_operation(
    operation,
    max_attempts=3,
    base_delay=1,
    sleep_func=None
):
    """
    Retry temporary connection and timeout failures
    using exponential backoff.
    """

    if max_attempts < 1:
        raise ValueError(
            "max_attempts must be at least 1"
        )

    if base_delay < 0:
        raise ValueError(
            "base_delay cannot be negative"
        )

    if sleep_func is None:
        sleep_func = time.sleep

    retryable_errors = (
        ConnectionError,
        TimeoutError,
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout
    )

    for attempt in range(1, max_attempts + 1):
        try:
            return operation()

        except retryable_errors:
            if attempt == max_attempts:
                raise

            delay = base_delay * (2 ** (attempt - 1))
            sleep_func(delay)
