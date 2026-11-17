import unittest
from unittest.mock import patch

from dashboard.app import app


class TestDashboardSyncHealth(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    @patch("dashboard.app.get_latest_sync")
    def test_successful_sync_health(self, mock_latest):
        mock_latest.return_value = {
            "sync_id": 1,
            "season": "2026/27",
            "status": "success",
            "successful_managers": 12,
            "failed_managers": 0,
            "started_at": "2026-11-16 12:00:00",
            "finished_at": "2026-11-16 12:01:00",
            "stage": None,
            "error_message": None,
            "failed_manager_ids": []
        }

        response = self.client.get("/api/sync/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["successful_managers"], 12)

    @patch("dashboard.app.get_latest_sync")
    def test_partial_sync_includes_failure_details(self, mock_latest):
        mock_latest.return_value = {
            "sync_id": 2,
            "season": "2026/27",
            "status": "partial",
            "successful_managers": 10,
            "failed_managers": 2,
            "started_at": "2026-11-16 12:00:00",
            "finished_at": "2026-11-16 12:01:00",
            "stage": "gameweeks",
            "error_message": "Two manager synchronizations failed",
            "failed_manager_ids": [953118, 1053858]
        }

        response = self.client.get("/api/sync/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "partial")
        self.assertEqual(response.json["stage"], "gameweeks")
        self.assertEqual(
            response.json["failed_manager_ids"],
            [953118, 1053858]
        )
        self.assertEqual(
            response.json["error_message"],
            "Two manager synchronizations failed"
        )

    @patch("dashboard.app.get_latest_sync")
    def test_no_sync_history(self, mock_latest):
        mock_latest.return_value = None

        response = self.client.get("/api/sync/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json["status"],
            "not_synchronized"
        )

    @patch("dashboard.app.get_latest_sync")
    def test_database_failure(self, mock_latest):
        mock_latest.side_effect = RuntimeError(
            "Database temporarily unavailable"
        )

        response = self.client.get("/api/sync/health")

        self.assertEqual(response.status_code, 503)
        self.assertEqual(
            response.json["error"],
            "Synchronization health is temporarily unavailable"
        )

    def test_system_health_page_renders(self):
        response = self.client.get("/system-health")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Synchronization Monitor",
            response.data
        )
        self.assertIn(
            b"Latest Synchronization",
            response.data
        )

    def test_system_health_page_loads_script(self):
        response = self.client.get("/system-health")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"js/sync_health.js",
            response.data
        )

    def test_system_health_navigation_link(self):
        response = self.client.get("/system-health")

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b'href="/system-health"',
            response.data
        )
        self.assertIn(
            b"System Health",
            response.data
        )
    @patch("dashboard.app.get_latest_sync")
    def test_api_includes_freshness(self, mock_latest):
        from datetime import datetime, timedelta, timezone

        finished_at = (
            datetime.now(timezone.utc) - timedelta(hours=72)
        ).isoformat()

        mock_latest.return_value = {
            "sync_id": 3,
            "season": "2026/27",
            "status": "success",
            "successful_managers": 12,
            "failed_managers": 0,
            "started_at": finished_at,
            "finished_at": finished_at,
            "stage": None,
            "error_message": None,
            "failed_manager_ids": None
        }

        response = self.client.get("/api/sync/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["freshness"], "stale")
        self.assertGreaterEqual(
            response.json["age_hours"], 72
        )

    @patch("dashboard.app.get_latest_sync")
    def test_api_preserves_existing_sync_fields(self, mock_latest):
        from datetime import datetime, timezone

        timestamp = datetime.now(timezone.utc).isoformat()

        mock_latest.return_value = {
            "sync_id": 4,
            "season": "2026/27",
            "status": "success",
            "successful_managers": 12,
            "failed_managers": 0,
            "started_at": timestamp,
            "finished_at": timestamp,
            "stage": None,
            "error_message": None,
            "failed_manager_ids": None
        }

        response = self.client.get("/api/sync/health")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.assertEqual(response.json["successful_managers"], 12)
        self.assertEqual(response.json["freshness"], "fresh")
        self.assertIn("age_hours", response.json)

    def test_system_health_page_has_freshness_card(self):
        response = self.client.get("/system-health")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Data Freshness", response.data)
        self.assertIn(b'id="sync-freshness"', response.data)
        self.assertIn(b'id="sync-age"', response.data)

if __name__ == "__main__":
    unittest.main()