import unittest
from unittest.mock import patch

from dashboard.app import app


class TestDashboardLeaderboard(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    @patch("dashboard.app.get_league_members")
    @patch("dashboard.app.get_league")
    @patch("dashboard.app.get_database_leaderboard", create=True)
    def test_league_dashboard_displays_rankings(
        self,
        mock_leaderboard,
        mock_league,
        mock_members
    ):
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


if __name__ == "__main__":
    unittest.main()