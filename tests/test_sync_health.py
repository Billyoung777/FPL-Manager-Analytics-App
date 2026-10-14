import unittest
from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import patch

from database.sync_health import show_sync_health


class TestSyncHealth(unittest.TestCase):

    @patch("database.sync_health.get_latest_sync")
    def test_no_sync_history(self, mock_get_latest_sync):
        """Health report handles an empty synchronization history."""

        mock_get_latest_sync.return_value = None

        output = StringIO()

        with redirect_stdout(output):
            show_sync_health()

        report = output.getvalue()

        self.assertIn(
            "No synchronization history found.",
            report
        )

        self.assertIn(
            "Database Status: NOT YET SYNCHRONIZED",
            report
        )

        mock_get_latest_sync.assert_called_once()


    @patch("database.sync_health.get_latest_sync")
    def test_successful_sync_health(self, mock_get_latest_sync):
        """Health report displays a successful synchronization."""

        mock_get_latest_sync.return_value = {
            "sync_id": 1,
            "season": "2026/27",
            "status": "success",
            "successful_managers": 12,
            "failed_managers": 0,
            "started_at": "2026-10-14 10:00:00",
            "finished_at": "2026-10-14 10:01:00"
        }

        output = StringIO()

        with redirect_stdout(output):
            show_sync_health()

        report = output.getvalue()

        self.assertIn("Season: 2026/27", report)
        self.assertIn("Status: SUCCESS", report)
        self.assertIn("Successful Managers: 12", report)
        self.assertIn("Failed Managers: 0", report)
        self.assertIn("Database Status: HEALTHY", report)

        mock_get_latest_sync.assert_called_once()


    @patch("database.sync_health.get_latest_sync")
    def test_partial_sync_health(self, mock_get_latest_sync):
        """Health report identifies partial synchronization."""

        mock_get_latest_sync.return_value = {
            "sync_id": 2,
            "season": "2026/27",
            "status": "partial",
            "successful_managers": 10,
            "failed_managers": 2,
            "started_at": "2026-10-14 11:00:00",
            "finished_at": "2026-10-14 11:02:00"
        }

        output = StringIO()

        with redirect_stdout(output):
            show_sync_health()

        report = output.getvalue()

        self.assertIn("Season: 2026/27", report)
        self.assertIn("Status: PARTIAL", report)
        self.assertIn("Successful Managers: 10", report)
        self.assertIn("Failed Managers: 2", report)
        self.assertIn(
            "Database Status: PARTIAL - ATTENTION REQUIRED",
            report
        )

        mock_get_latest_sync.assert_called_once()


    @patch("database.sync_health.get_latest_sync")
    def test_failed_sync_health(self, mock_get_latest_sync):
        """Health report identifies failed synchronization."""

        mock_get_latest_sync.return_value = {
            "sync_id": 3,
            "season": "2026/27",
            "status": "failed",
            "successful_managers": 0,
            "failed_managers": 0,
            "started_at": "2026-10-14 12:00:00",
            "finished_at": "2026-10-14 12:01:00"
        }

        output = StringIO()

        with redirect_stdout(output):
            show_sync_health()

        report = output.getvalue()

        self.assertIn("Season: 2026/27", report)
        self.assertIn("Status: FAILED", report)
        self.assertIn("Successful Managers: 0", report)
        self.assertIn("Failed Managers: 0", report)
        self.assertIn(
            "Database Status: FAILED - ATTENTION REQUIRED",
            report
        )

        mock_get_latest_sync.assert_called_once()


if __name__ == "__main__":
    unittest.main()
