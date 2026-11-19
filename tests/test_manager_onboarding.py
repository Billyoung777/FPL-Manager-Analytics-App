
import unittest
from unittest.mock import patch

from dashboard.app import app


class TestManagerOnboarding(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("dashboard.app.sync_gameweeks")
    @patch("dashboard.app.register_manager_leagues")
    def test_valid_manager_triggers_initial_sync(
        self, mock_register, mock_sync
    ):
        response = self.client.get("/enter?id=1053858")

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "/manager?id=1053858",
            response.headers["Location"]
        )

        mock_register.assert_called_once_with(1053858)
        mock_sync.assert_called_once_with(
            1053858, "2026/27"
        )

    @patch("dashboard.app.sync_gameweeks")
    @patch("dashboard.app.register_manager_leagues")
    def test_invalid_manager_id(
        self, mock_register, mock_sync
    ):
        response = self.client.get("/enter?id=-1")

        self.assertEqual(response.status_code, 400)
        mock_register.assert_not_called()
        mock_sync.assert_not_called()

    @patch("dashboard.app.sync_gameweeks")
    @patch("dashboard.app.register_manager_leagues")
    def test_sync_failure_preserves_registration(
        self, mock_register, mock_sync
    ):
        mock_sync.side_effect = RuntimeError(
            "FPL API temporarily unavailable"
        )

        response = self.client.get("/enter?id=1053858")

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "/manager?id=1053858",
            response.headers["Location"]
        )

        mock_register.assert_called_once_with(1053858)

        with self.client.session_transaction() as session:
            self.assertEqual(
                session["manager_id"], 1053858
            )


if __name__ == "__main__":
    unittest.main()
