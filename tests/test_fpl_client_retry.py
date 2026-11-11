
import unittest
from unittest.mock import Mock, patch

import requests

from api.fpl_client import FPLClient


class TestFPLClientRetry(unittest.TestCase):

    @patch("api.retry.time.sleep")
    @patch("api.fpl_client.requests.get")
    def test_connection_failure_then_success(
        self,
        mock_get,
        mock_sleep
    ):
        response = Mock()
        response.json.return_value = {"ok": True}

        mock_get.side_effect = [
            requests.exceptions.ConnectionError(
                "Connection reset"
            ),
            response
        ]

        client = FPLClient(timeout=5)

        result = client.get("bootstrap-static/")

        self.assertEqual(result, {"ok": True})
        self.assertEqual(mock_get.call_count, 2)
        mock_sleep.assert_called_once_with(1)

    @patch("api.retry.time.sleep")
    @patch("api.fpl_client.requests.get")
    def test_timeout_exhausts_retries(
        self,
        mock_get,
        mock_sleep
    ):
        mock_get.side_effect = (
            requests.exceptions.Timeout("Timed out")
        )

        client = FPLClient(timeout=5)

        with self.assertRaisesRegex(
            RuntimeError,
            "timed out"
        ):
            client.get("bootstrap-static/")

        self.assertEqual(mock_get.call_count, 3)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("api.retry.time.sleep")
    @patch("api.fpl_client.requests.get")
    def test_http_404_not_retried(
        self,
        mock_get,
        mock_sleep
    ):
        response = Mock()

        response.raise_for_status.side_effect = (
            requests.exceptions.HTTPError(
                "404 Client Error"
            )
        )

        mock_get.return_value = response

        client = FPLClient()

        with self.assertRaisesRegex(
            RuntimeError,
            "HTTP error"
        ):
            client.get("entry/999999/history/")

        self.assertEqual(mock_get.call_count, 1)
        mock_sleep.assert_not_called()


if __name__ == "__main__":
    unittest.main()
