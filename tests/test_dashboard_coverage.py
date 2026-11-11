
import unittest
from unittest.mock import patch

from dashboard.app import app


class TestDashboardCoverage(unittest.TestCase):

    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def get_dashboard(self, coverage, statuses=None, api_error=None):
        league = {
            "league_id": 100,
            "league_name": "Test League"
        }

        members = [{"manager_id": 1}]

        leaderboard = (
            "Test League",
            [{
                "rank": 1,
                "manager_id": 1,
                "manager_name": "Manager One",
                "team_name": "Team One",
                "gameweeks": 2,
                "total_points": 106,
                "average_points": 53.0
            }]
        )

        if statuses is None:
            statuses = [
                {"gameweek": 1, "verified": True},
                {"gameweek": 2, "verified": True},
                {"gameweek": 3, "verified": True}
            ]

        with (
            patch("dashboard.app.get_league", return_value=league),
            patch("dashboard.app.get_league_members", return_value=members),
            patch(
                "dashboard.app.get_database_leaderboard",
                return_value=leaderboard
            ),
            patch("dashboard.app.get_gameweek_statuses") as mock_statuses,
            patch(
                "dashboard.app.get_manager_completeness",
                return_value=coverage
            ) as mock_completeness
        ):
            if api_error is not None:
                mock_statuses.side_effect = api_error
            else:
                mock_statuses.return_value = statuses

            response = self.client.get(
                "/league/100?manager_id=1"
            )

            return response, mock_completeness.call_args

    def test_complete_coverage(self):
        response, call = self.get_dashboard({
            "status": "complete",
            "missing_gameweeks": []
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Complete",
            response.get_data(as_text=True)
        )
        self.assertEqual(call.args[2], [1, 2, 3])

    def test_incomplete_coverage(self):
        response, _ = self.get_dashboard({
            "status": "incomplete",
            "missing_gameweeks": [2, 3]
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "Missing 2 GW",
            response.get_data(as_text=True)
        )

    def test_no_stored_history(self):
        response, _ = self.get_dashboard({
            "status": "not_synchronized",
            "missing_gameweeks": [1, 2, 3]
        })

        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "No history",
            response.get_data(as_text=True)
        )

    def test_api_failure_shows_unknown(self):
        response, call = self.get_dashboard(
            {
                "status": "unknown",
                "missing_gameweeks": []
            },
            api_error=RuntimeError("FPL API unavailable")
        )

        self.assertEqual(response.status_code, 200)

        html = response.get_data(as_text=True)

        self.assertIn("Unknown", html)
        self.assertIn("Team One", html)
        self.assertEqual(call.args[2], None)

    def test_table_column_order(self):
        response, _ = self.get_dashboard({
            "status": "complete",
            "missing_gameweeks": []
        })

        html = response.get_data(as_text=True)

        headings = [
            "<th>GW Recorded</th>",
            "<th>Data Coverage</th>",
            "<th>Net Points</th>",
            "<th>Average / GW</th>"
        ]

        positions = [html.index(heading) for heading in headings]

        self.assertEqual(positions, sorted(positions))

        self.assertLess(
            html.index('class="coverage-complete"'),
            html.index("<strong>106</strong>")
        )


if __name__ == "__main__":
    unittest.main()
