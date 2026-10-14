
import unittest
from unittest.mock import patch

from database.sync_all import record_sync_result


class TestSyncHistoryLogging(unittest.TestCase):

    @patch("database.sync_all.get_sync_timestamp")
    @patch("database.sync_all.save_sync_history")
    def test_successful_sync_logging(
        self,
        mock_save,
        mock_timestamp
    ):
        mock_timestamp.return_value = "2026-10-14 13:30:00"

        result = {
            "status": "success",
            "season": "2026/27",
            "successful_managers": 12,
            "failed_managers": []
        }

        returned_result = record_sync_result(
            result,
            started_at="2026-10-14 13:29:00"
        )

        mock_save.assert_called_once_with(
            season="2026/27",
            status="success",
            successful_managers=12,
            failed_managers=0,
            started_at="2026-10-14 13:29:00",
            finished_at="2026-10-14 13:30:00"
        )

        self.assertEqual(returned_result, result)


    @patch("database.sync_all.get_sync_timestamp")
    @patch("database.sync_all.save_sync_history")
    def test_partial_sync_logging(
        self,
        mock_save,
        mock_timestamp
    ):
        mock_timestamp.return_value = "2026-10-14 13:35:00"

        result = {
            "status": "partial",
            "season": "2026/27",
            "successful_managers": 10,
            "failed_managers": [953118, 1053858]
        }

        returned_result = record_sync_result(
            result,
            started_at="2026-10-14 13:34:00"
        )

        mock_save.assert_called_once_with(
            season="2026/27",
            status="partial",
            successful_managers=10,
            failed_managers=2,
            started_at="2026-10-14 13:34:00",
            finished_at="2026-10-14 13:35:00"
        )

        self.assertEqual(returned_result, result)


    @patch("database.sync_all.get_sync_timestamp")
    @patch("database.sync_all.save_sync_history")
    def test_failed_sync_logging(
        self,
        mock_save,
        mock_timestamp
    ):
        mock_timestamp.return_value = "2026-10-14 13:40:00"

        result = {
            "status": "failed",
            "season": "2026/27",
            "stage": "leagues",
            "successful_leagues": 0,
            "failed_leagues": [1701837, 1840079]
        }

        returned_result = record_sync_result(
            result,
            started_at="2026-10-14 13:39:00"
        )

        mock_save.assert_called_once_with(
            season="2026/27",
            status="failed",
            successful_managers=0,
            failed_managers=0,
            started_at="2026-10-14 13:39:00",
            finished_at="2026-10-14 13:40:00"
        )

        self.assertEqual(returned_result, result)


if __name__ == "__main__":
    unittest.main()
