
import unittest
from unittest.mock import patch

from dashboard.app import app


class TestDashboardSyncHistory(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @patch("dashboard.app.get_recent_syncs")
    def test_history_api_returns_records(self, mock_recent):
        mock_recent.return_value = [
            {
                "sync_id": 2,
                "season": "2026/27",
                "status": "partial",
                "successful_managers": 10,
                "failed_managers": 2,
                "started_at": "2026-11-16 10:00:00",
                "finished_at": "2026-11-16 10:01:00",
                "stage": "gameweeks",
                "error_message": "Two managers failed",
                "failed_manager_ids": [953118, 1053858]
            },
            {
                "sync_id": 1,
                "season": "2026/27",
                "status": "success",
                "successful_managers": 12,
                "failed_managers": 0,
                "started_at": "2026-11-15 10:00:00",
                "finished_at": "2026-11-15 10:01:00",
                "stage": None,
                "error_message": None,
                "failed_manager_ids": None
            }
        ]

        response = self.client.get("/api/sync/history?limit=5")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["count"], 2)
        self.assertEqual(len(response.json["history"]), 2)
        self.assertEqual(response.json["history"][0]["sync_id"], 2)
        self.assertEqual(
            response.json["history"][0]["failed_manager_ids"],
            [953118, 1053858]
        )
        mock_recent.assert_called_once_with(limit=5)

    @patch("dashboard.app.get_recent_syncs")
    def test_history_api_empty(self, mock_recent):
        mock_recent.return_value = []

        response = self.client.get("/api/sync/history")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            "count": 0,
            "history": []
        })
        mock_recent.assert_called_once_with(limit=10)

    @patch("dashboard.app.get_recent_syncs")
    def test_history_api_invalid_limits(self, mock_recent):
        invalid_limits = [
            "0", "-1", "101", "abc", "2.5", ""
        ]

        for limit in invalid_limits:
            with self.subTest(limit=limit):
                response = self.client.get(
                    "/api/sync/history",
                    query_string={"limit": limit}
                )
                self.assertEqual(response.status_code, 400)
                self.assertIn("error", response.json)

        mock_recent.assert_not_called()

    @patch("dashboard.app.get_recent_syncs")
    def test_history_api_database_failure(self, mock_recent):
        mock_recent.side_effect = RuntimeError(
            "Database temporarily unavailable"
        )

        response = self.client.get("/api/sync/history")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json["error"],
            "Synchronization history is temporarily unavailable"
        )

    def test_system_health_page_contains_history_table(self):
        response = self.client.get("/system-health")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Synchronization History",
            response.data
        )
        self.assertIn(
            b'id="sync-history-body"',
            response.data
        )
        self.assertIn(
            b'id="sync-history-message"',
            response.data
        )
        self.assertIn(
            b"js/sync_history.js",
            response.data
        )


if __name__ == "__main__":
    unittest.main()
