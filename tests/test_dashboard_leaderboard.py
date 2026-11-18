import unittest
from unittest.mock import patch

from dashboard.app import app


class TestDashboardLeaderboard(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()



    @patch("dashboard.app.get_manager_completeness")
    @patch("dashboard.app.get_gameweek_statuses")
    @patch("dashboard.app.get_league_members")
    @patch("dashboard.app.get_league")
    @patch("dashboard.app.get_database_leaderboard")
    def test_league_dashboard_displays_rankings(
        self,
        mock_leaderboard,
        mock_league,
        mock_members,
        mock_statuses,
        mock_completeness
    ):
        mock_statuses.return_value = [
            {"gameweek": 1, "verified": True},
            {"gameweek": 2, "verified": True}
        ]

        mock_completeness.return_value = {
            "status": "complete",
            "missing_gameweeks": [],
            "stored_count": 2,
            "expected_count": 2
        }

        mock_league.return_value = {
            "league_id": 100,
            "league_name": "Test League"
        }

        mock_members.return_value = [
            {"manager_id": 1},
            {"manager_id": 2}
        ]

        mock_leaderboard.return_value = (
            "Test League",
            [
                {
                    "rank": 1,
                    "manager_id": 2,
                    "manager_name": "Manager Two",
                    "team_name": "Team Two",
                    "gameweeks": 2,
                    "total_points": 120,
                    "average_points": 60.0
                },
                {
                    "rank": 2,
                    "manager_id": 1,
                    "manager_name": "Manager One",
                    "team_name": "Team One",
                    "gameweeks": 2,
                    "total_points": 106,
                    "average_points": 53.0
                }
            ]
        )

        response = self.client.get(
            "/league/100?manager_id=1"
        )

        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)

        self.assertIn("Team Two", html)
        self.assertIn("120", html)
        self.assertIn("Team One", html)
        self.assertIn("106", html)

        mock_leaderboard.assert_called_once_with(
            100,
            "2026/27",
            mode="provisional"
        )


    @patch("dashboard.app.synchronize_league_members")
    @patch("dashboard.app.get_league_members")
    def test_refresh_preserves_verified_mode(
        self,
        mock_members,
        mock_sync
    ):
        mock_members.return_value = [
            {"manager_id": 1}
        ]

        response = self.client.post(
            "/league/100/refresh",
            data={
                "manager_id": "1",
                "mode": "verified"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "mode=verified",
            response.headers["Location"]
        )
        self.assertIn(
            "manager_id=1",
            response.headers["Location"]
        )
        mock_sync.assert_called_once_with(100)

    @patch("dashboard.app.synchronize_league_members")
    @patch("dashboard.app.get_league_members")
    def test_refresh_preserves_provisional_mode(
        self,
        mock_members,
        mock_sync
    ):
        mock_members.return_value = [
            {"manager_id": 1}
        ]

        response = self.client.post(
            "/league/100/refresh",
            data={
                "manager_id": "1",
                "mode": "provisional"
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertIn(
            "mode=provisional",
            response.headers["Location"]
        )
        mock_sync.assert_called_once_with(100)

    @patch("dashboard.app.synchronize_league_members")
    @patch("dashboard.app.get_league_members")
    def test_refresh_rejects_invalid_mode(
        self,
        mock_members,
        mock_sync
    ):
        mock_members.return_value = [
            {"manager_id": 1}
        ]

        response = self.client.post(
            "/league/100/refresh",
            data={
                "manager_id": "1",
                "mode": "invalid"
            }
        )

        self.assertEqual(response.status_code, 400)
        mock_sync.assert_not_called()

if __name__ == "__main__":
    unittest.main()