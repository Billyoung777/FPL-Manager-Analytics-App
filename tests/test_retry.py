
import unittest
from unittest.mock import Mock

from api.retry import retry_operation


class TestRetryOperation(unittest.TestCase):

    def test_success_without_retry(self):
        operation = Mock(return_value="OK")
        sleep = Mock()

        result = retry_operation(
            operation,
            sleep_func=sleep
        )

        self.assertEqual(result, "OK")
        self.assertEqual(operation.call_count, 1)
        sleep.assert_not_called()

    def test_retries_then_succeeds(self):
        operation = Mock(side_effect=[
            ConnectionError("Connection reset"),
            TimeoutError("Timed out"),
            "OK"
        ])
        sleep = Mock()

        result = retry_operation(
            operation,
            sleep_func=sleep
        )

        self.assertEqual(result, "OK")
        self.assertEqual(operation.call_count, 3)
        self.assertEqual(
            [call.args[0] for call in sleep.call_args_list],
            [1, 2]
        )

    def test_stops_after_max_attempts(self):
        operation = Mock(
            side_effect=ConnectionError("Unavailable")
        )
        sleep = Mock()

        with self.assertRaises(ConnectionError):
            retry_operation(
                operation,
                max_attempts=3,
                sleep_func=sleep
            )

        self.assertEqual(operation.call_count, 3)
        self.assertEqual(sleep.call_count, 2)

    def test_does_not_retry_programming_errors(self):
        operation = Mock(
            side_effect=ValueError("Invalid data")
        )
        sleep = Mock()

        with self.assertRaises(ValueError):
            retry_operation(
                operation,
                sleep_func=sleep
            )

        self.assertEqual(operation.call_count, 1)
        sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
