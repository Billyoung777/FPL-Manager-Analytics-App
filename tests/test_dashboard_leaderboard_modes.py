
import unittest
from unittest.mock import patch

from dashboard.app import app


class TestDashboardLeaderboardModes(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

        self.patchers = [
            patch("dashboard.app.get_league"),
            patch("dashboard.app.get_league_members"),
            patch("dashboard.app.get_database_leaderboard"),
            patch("dashboard.app.get_gameweek_statuses"),
            patch("dashboard.app.get_manager_completeness"),
        ]

        (
            self.mock_league,
            self.mock_members,
            self.mock_leaderboard,
            self.mock_statuses,
            self.mock_completeness,
        ) = [patcher.start() for patcher in self.patchers]

        self.mock_league.return_value = {
            "league_id": 100,
            "league_name": "Test League",
        }

        self.mock_members.return_value = [
            {"manager_id": 1}
        ]

        self.mock_leaderboard.return_value = (
            "Test League",
            [{
                "rank": 1,
                "manager_id": 1,
                "manager_name": "Manager One",
                "team_name": "Team One",
                "gameweeks": 2,
                "total_points": 106,
                "average_points": 53.0,
            }]
        )

        self.mock_statuses.return_value = [
            {"gameweek": 1, "verified": True},
            {"gameweek": 2, "verified": False},
        ]

        self.mock_completeness.return_value = {
            "status": "complete",
            "missing_gameweeks": [],
            "stored_count": 1,
            "expected_count": 1,
        }

    def tearDown(self):
        for patcher in reversed(self.patchers):
            patcher.stop()

    def test_default_mode_is_provisional(self):
        response = self.client.get(
            "/league/100?manager_id=1"
        )

        self.assertEqual(response.status_code, 200)
        self.mock_leaderboard.assert_called_once_with(
            100, "2026/27", mode="provisional"
        )

    def test_explicit_provisional_mode(self):
        response = self.client.get(
            "/league/100?manager_id=1&mode=provisional"
        )

        self.assertEqual(response.status_code, 200)
        self.mock_leaderboard.assert_called_once_with(
            100, "2026/27", mode="provisional"
        )

    def test_verified_mode_reuses_gameweek_ids(self):
        response = self.client.get(
            "/league/100?manager_id=1&mode=verified"
        )

        self.assertEqual(response.status_code, 200)

        self.mock_leaderboard.assert_called_once_with(
            100,
            "2026/27",
            mode="verified",
            verified_gameweeks=[1]
        )

        self.mock_statuses.assert_called_once_with()

    def test_invalid_mode_returns_400(self):
        response = self.client.get(
            "/league/100?manager_id=1&mode=invalid"
        )

        self.assertEqual(response.status_code, 400)
        self.mock_leaderboard.assert_not_called()

    def test_verified_mode_returns_503_when_api_fails(self):
        self.mock_statuses.side_effect = RuntimeError(
            "FPL API unavailable"
        )

        response = self.client.get(
            "/league/100?manager_id=1&mode=verified"
        )

        self.assertEqual(response.status_code, 503)
        self.mock_leaderboard.assert_not_called()

    def test_provisional_mode_survives_api_failure(self):
        self.mock_statuses.side_effect = RuntimeError(
            "FPL API unavailable"
        )

        response = self.client.get(
            "/league/100?manager_id=1&mode=provisional"
        )

        self.assertEqual(response.status_code, 200)

        self.mock_leaderboard.assert_called_once_with(
            100, "2026/27", mode="provisional"
        )

        self.mock_completeness.assert_called_once_with(
            1, "2026/27", None
        )


if __name__ == "__main__":
    unittest.main()
